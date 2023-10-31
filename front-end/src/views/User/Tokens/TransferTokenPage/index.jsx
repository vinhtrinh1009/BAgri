import React, { useEffect, useState, useRef } from "react"
import { Container, Row, Col, Card, CardHeader, CardBody, Label } from 'reactstrap'
import { Spinner, Badge, Form } from "react-bootstrap"
// import { TextField, Button } from "@mui/material";
import { TextField, MenuItem, Button, FormControl, InputLabel, Select, } from '@mui/material'; 
import { LoadingButton } from '@mui/lab';
import Web3 from 'web3';
import { invokeBurnTransactionV2, invokeTransaction, getFabricTokensByNetwork, getFabricNetworks, getNetworks, getTokenByNetwork, getBridgeContractInterface, getERC20ContractInterface } from "src/services/User/tokens";
import { setToken } from "src/utils/token";

const TransferTokenPage = () => {
    const [connected, setConnected] = useState(false);
    const [connecting, setConnecting] = useState(false);
    const [loading, setLoading] = useState(false);
    const [enableSubmit, setEnableSubmit] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const [transfering, setTransfering] = useState(false);

    const [networks, setNetworks] = useState([]);
    const [fromTokens, setFromTokens] = useState([]);
    const [toTokens, setToTokens] = useState([]);

    const [fromNetworkType, setFromNetworkType] = useState('')
    const [fromNetworks, setFromNetworks] = useState([])
    
    const [toNetworkType, setToNetworkType] = useState('')
    const [toNetworks, setToNetworks] = useState([])

    const [accountAddress, setAccountAddress] = useState(undefined);

    const [fromNetwork, setFromNetwork] = useState(undefined);
    const [toNetwork, setToNetwork] = useState(undefined);

    const [fromToken, setFromToken] = useState(undefined);
    const [toToken, setToToken] = useState(undefined);

    const [amount, setAmount] = useState(0);
    const [maxAmount, setMaxAmount] = useState(0);
    const [toAddress, setToAddress] = useState('');

    const [username, setUsername] = useState(undefined)
    const [password, setPassword] = useState(undefined)
    const [fromOrganizations, setFromOrganizations] = useState([])
    const [organization, setOrganization] = useState(undefined)

    const [minter_orgs, setMinterOrgs] = useState([])
    const [minter_org, setMinterOrg] = useState(undefined)
    const [minter_username, setMinterUsername] = useState(undefined)

    const web3Ref = useRef(undefined);

    const rinkebyBridgeContractInterfaceRef = useRef(undefined);
    const goerliBridgeContractInterfaceRef = useRef(undefined);
    const erc20ContractInterfaceRef = useRef(undefined);

    useEffect(() => {
        getNetworks().then(res => {
            setNetworks(res.data);

            setFromNetworks(res.data);
            if(res.data.length > 0){
                setFromNetwork(res.data[0]);
            }
            setToNetworks(res.data);
            if(res.data.length > 0){
                setToNetwork(res.data[0]);
            }
        })

        getBridgeContractInterface({network: "Rinkeby Test Network"}).then(res => {
            rinkebyBridgeContractInterfaceRef.current = res.data;
        })

        getBridgeContractInterface({network: "Goerli Test Network"}).then(res => {
            goerliBridgeContractInterfaceRef.current = res.data;
        })

        getERC20ContractInterface().then(res => {
            erc20ContractInterfaceRef.current = res.data;
        })
    }, [])

    useEffect(() => {
        if(fromToken && toToken && amount > 0 && (toAddress||toNetworkType==='user_defined_network')) setEnableSubmit(true);
        else setEnableSubmit(false);
    }, [fromToken, toToken, amount, toAddress, fromNetworkType, toNetworkType])

    useEffect(() => {
        if(!fromNetwork) return;
        if(fromNetworkType==='injected_network'){
            getTokenByNetwork({network_name: fromNetwork.name}).then(res => {
                setFromTokens(res.data.results.filter(token => token.address));
                setFromToken(undefined);
            })
        }
        if(fromNetworkType==='user_defined_network'){
            getFabricTokensByNetwork({network: fromNetwork.network_id}).then(res => {
                setFromTokens(res.data);
                setFromToken(undefined);
            })
            setFromOrganizations(fromNetwork.blockchain_peer_config.organizations)
        }
        
    }, [fromNetwork, fromOrganizations])

    useEffect(() => {
        if(!toNetwork) return;

        if(!fromToken){
            setToToken(undefined);
            setToNetwork(undefined);
            return
        }
        if(toNetworkType==='injected_network'){
            getTokenByNetwork({network_name: toNetwork.name, linked_contract: fromToken.id}).then(res => {
                setToTokens(res.data.results);
                if(res.data.results.length > 0) setToToken(res.data.results[0]);
                else setToToken(undefined);
            })
        }
        if(toNetworkType==='user_defined_network'){
            getFabricTokensByNetwork({network: toNetwork.network_id, linked_token: fromToken.id}).then(res => {
                setToTokens(res.data);
                if(res.data.length > 0) setToToken(res.data[0]);
                else setToToken(undefined);
            })
            setMinterOrgs(toNetwork.blockchain_peer_config.organizations)
        }
            
        
    }, [toNetwork, fromToken])

    useEffect(() => {
        if(!fromToken || !accountAddress){
            setMaxAmount('');
            return;
        };
        if(!fromToken.address){
            setMaxAmount(''); return;
        }

        async function getBalance(){
            const accounts = await web3Ref.current.eth.getAccounts();
            const contract = await new web3Ref.current.eth.Contract(erc20ContractInterfaceRef.current, fromToken.address);
            const _balance = await contract.methods.balanceOf(accounts[0]).call();
            const BN = web3Ref.current.utils.BN;
            let balance = new BN(_balance);

            setMaxAmount(balance.div((new BN(10)).pow(new BN(fromToken.decimal))).toNumber());
        }

        getBalance();

    }, [fromToken])

    useEffect(() => {
        if(maxAmount === '' || maxAmount === undefined) return;

        if(amount > maxAmount){
            setErrorMessage('Warning: Amount is too high');
        }
        else setErrorMessage('');

    }, [amount])

    const handleFromNetworkTypeChange = (e) => {
        let value = e.target.value
        setFromNetworkType(value);

        if(value === 'injected_network'){
            getNetworks().then(res => {
                setFromNetworks(res.data);
                if(res.data.length > 0){
                    setFromNetwork(res.data[0]);
                }
            })
            setConnecting(true);
            window.ethereum.request({method: 'eth_requestAccounts'}).then(res => {
            web3Ref.current = new Web3(window.ethereum);

            if(res.length > 0) setAccountAddress(res[0]);

            setConnected(true);
            setConnecting(false);
        });
        }
        else if(value === 'user_defined_network'){
            getFabricNetworks().then(res => {
                setFromNetworks(res.data);
                if(res.data.length > 0){
                    setFromNetwork(res.data[0]);
                }
            })
            setConnected(false)
            setConnecting(false)
        }
    }

    const handleToNetworkTypeChange = (e) => {
        let value = e.target.value
        setToNetworkType(value);

        if(value === 'injected_network'){
            getNetworks().then(res => {
                setToNetworks(res.data);
                if(res.data.length > 0){
                    setToNetwork(res.data[0]);
                }
            })
        }
        else if(value === 'user_defined_network'){
            getFabricNetworks().then(res => {
                setToNetworks(res.data);
                if(res.data.length > 0){
                    setToNetwork(res.data[0]);
                }
            })
        }
    }

    const handleConnectButtonClick = () => {
        setConnecting(true);
        window.ethereum.request({method: 'eth_requestAccounts'}).then(res => {
            web3Ref.current = new Web3(window.ethereum);

            if(res.length > 0) setAccountAddress(res[0]);

            setConnected(true);
            setConnecting(false);
        });
    }

    async function handleSubmit(){
        if (fromNetworkType === 'injected_network'){
            const accounts = await web3Ref.current.eth.getAccounts();

            console.log("Attempt to send transaction from account", accounts[0]);
            
            // need abi and bin
    
            setTransfering(true);
    
            console.log(rinkebyBridgeContractInterfaceRef.current);
    
            try{
                let contract = undefined;
                if(fromNetwork.name === 'Rinkeby Test Network'){
                    contract = await new web3Ref.current.eth.Contract(rinkebyBridgeContractInterfaceRef.current, "0x3557bCE70d478F73647110A9Cb41e57926dD64C3");
                }
                else if(fromNetwork.name === 'Goerli Test Network'){
                    contract = await new web3Ref.current.eth.Contract(goerliBridgeContractInterfaceRef.current, "0x4b4E91159E41d614294d8f2EEcC700d13C342528");
                }
                else{
                    alert("Unsupported network");
                    return;
                }
                const BN = web3Ref.current.utils.BN;
                const tx = contract.methods.burn(fromToken.address, !toAddress ? "0x0000000000000000000000000000000000000000" : toAddress, new BN(amount).mul(new BN(10).pow(new BN(fromToken.decimal))));
    
                // await tx.send({from: accounts[0], gas: "210000" });
                await tx.send({from: accounts[0]});
    
                let newMaxAmount = maxAmount - amount;
    
                setMaxAmount(newMaxAmount);
                if(toNetworkType === 'user_defined_network'){
                    invokeTransaction({
                        token_name: toToken.token_name,
                        network_id: toNetwork.network_id,
                        quantity: amount
                    }).then(res => {
                        alert("Token is transferred successfully");
                        window.location.reload()
                    }).catch(err => {alert('Something wrong happens')})
                }
                setTransfering(false);
                alert("Token is transferred successfully");
                window.location.reload()
    
            } catch(error){
                console.log(error);
    
                alert("Something wrong happens. Please try again.");
                setTransfering(false);
            }
        }
        if (fromNetworkType==='user_defined_network'){
            setTransfering(true)
            invokeBurnTransactionV2({
                token_name: fromToken.token_name,
                network_name: fromNetwork.name,
                network_id:fromNetwork.network_id,
                quantity: amount*Math.pow(10, fromToken.decimal), 
                to_address: toAddress,
                to_token: toToken.address,
                to_network: toNetwork.network_id,
                username: username,
                passwd: password,
                org: organization,

            })
            .then(res => {
                setTransfering(false)
                alert('Transaction executed successfully')
                window.location.reload()
            })
            .catch(err => {
                alert('Something wrong happens. Please try again')
                setTransfering(false)
            })

        }
        
    }

    const handleFromNetworkChange = e => {
        const newFromNetwork = e.target.value;
        // console.log(newFromNetwork)

        if(!newFromNetwork){
            setFromNetwork(undefined);
            console.log('why')
        }

        for(let i=0; i<fromNetworks.length; i++){
            if(fromNetworks[i].name === newFromNetwork) setFromNetwork(fromNetworks[i]);
            console.log(fromNetwork)
        }
        // if(networks.length >= 2){
        //     for(let i=0; i<networks.length; i++){
        //         if(networks[i].name !== newFromNetwork) setToNetwork(networks[i]);
        //     }
        // }
    }

    const handleToNetworkChange = e => {
        const newToNetwork = e.target.value;
        if(!newToNetwork){
            setFromNetwork(undefined);
            console.log('why')
        }
        for(let i=0; i<toNetworks.length; i++){
            if(toNetworks[i].name === newToNetwork) setToNetwork(toNetworks[i]);
        }
    }

    const handleFromTokenChange = e => {
        const newFromTokenId = e.target.value;
        console.log(newFromTokenId)

        if(!newFromTokenId) setFromToken(undefined)
        else{
            for(let i=0; i< fromTokens.length; i++){
                console.log(fromTokens[i].id)
                if(fromTokens[i].id == newFromTokenId) {
                    console.log(fromTokens[i])
                    setFromToken(fromTokens[i]);

                }
            }
        }
    }

    const handleToTokenChange = e => {
        const newToTokenId = e.target.value;

        if(!newToTokenId) setToToken(undefined);
        else{
            for(let i=0; i< toTokens.length; i++){
                if(toTokens[i].id == newToTokenId) setToToken(toTokens[i]);
            }
        }
    }

    const handleAmountChange = e => {
        setAmount(e.target.value);
    }

    const handleToAddressChange = e => {
        setToAddress(e.target.value);
    }

    function handleUsernameChange(e) {
        setUsername(e.target.value)
    }

    function handlePasswordChange(e) {
        setPassword(e.target.value)
    }

    function handleOrgChange(e){
        setOrganization(e.target.value)
    }

    function handleMinterOrgChange(e){
        setMinterOrg(e.target.value)
    }

    function handleMinterUsernameChange(e){
        setMinterUsername(e.target.value)
    }

    const isSubmittable = () => {
        let res = connected && !transfering && enableSubmit;

        if(maxAmount !== '' && maxAmount !== undefined && amount){
            res = res & (amount <= maxAmount);
            return res
        }
        if (fromNetworkType==='user_defined_network'){
            res=!transfering && enableSubmit
        }
        return res;
    }

    return (
        <>
            <Container>
                <Row className="pt-3">
                    <Col className="box-col-12">
                        <Card>
                            <CardHeader>
                                <h5>Transfer Token</h5>
                                <div className="media-body text-right">
                                </div>
                            </CardHeader>

                            <CardBody>
                               
                                {/* <div className="d-flex justify-content-center w-100 flex-column align-items-center">
                                    <LoadingButton variant={connected ? "contained" : "outlined" } 
                                                    className="px-2 mb-2 mr-2 text-nowrap" 
                                                    onClick={handleConnectButtonClick} 
                                                    loading={loading}
                                                    disableElevation={true}>
                                                    {connected ? `Connected to ${accountAddress ? (accountAddress.substring(0, 6) + '...' + accountAddress.substring(accountAddress.length-4, accountAddress.length)) : ''}`:'Connect to wallet'}
                                    </LoadingButton>
                                </div> */}

                                <div className={"row mt-4 mx-5 justify-content-center " }>
                                    <div className="col col-5">
                                        <h5 className="text-center">From</h5>
                                        <div className="d-flex flex-row flex-wrap mb-1">
                                            <FormControl variant="filled" fullWidth style={{ marginBottom: "31px" }} required size="small">
                                                <InputLabel id="from-network-type">{"Select network type"}</InputLabel>

                                                <Select labelId="from-network-type" onChange={handleFromNetworkTypeChange}>
                                                    <MenuItem value={"user_defined_network"}>{"Use user defined network"}</MenuItem>
                                                    <MenuItem value={"injected_network"}>{"Use injected Ethereum network"}</MenuItem>
                                                </Select>
                                            </FormControl>   
                                        </div>
                                        <div className="mb-3">
                                            <Label>Network</Label>
                                            <FormControl variant="filled" fullWidth style={{ marginBottom: "31px" }} required size="small">
                                                <InputLabel id="from-network">{"Select network"}</InputLabel>

                                                <Select labelId="from-network" onChange={handleFromNetworkChange}>
                                                    {fromNetworks.map(network => (
                                                        <MenuItem key={network.network_id} value={network.network_id}>
                                                        {network.name}
                                                        </MenuItem>
                                                    ))}
                                                </Select>
                                            </FormControl>                                            
                                        </div>
                                        {fromNetworkType==='user_defined_network'?
                                            <Card>
                                                <CardHeader>
                                                    Fabric credential
                                                </CardHeader>
                                                <CardBody>
                                                    <div className="mb-3">
                                                        <Label>Organization</Label>
                                                        <FormControl variant="filled" fullWidth style={{ marginBottom: "31px" }} required size="small" disabled={fromNetworkType==='injected_network'}>
                                                            <InputLabel id="from-org">{"Select organization"}</InputLabel>

                                                            <Select labelId="from-org" onChange={handleOrgChange}>
                                                                {fromOrganizations.map(org => (
                                                                    <MenuItem key={org.name} value={org.name}>
                                                                    {org.name}
                                                                    </MenuItem>
                                                                ))}
                                                            </Select>
                                                        </FormControl>
                                                    </div>

                                                    <div className="mb-3">
                                                        <Label>Username</Label>
                                                        <TextField type="text" value={username} onChange={handleUsernameChange} disabled={fromNetworkType==='injected_network'} fullWidth className="mb-3"></TextField>
                                                    </div>
                                                    
                                                    <div className="mb-3">
                                                        <Label>Password</Label>
                                                        <TextField type="text" value={password} onChange={handlePasswordChange} disabled={fromNetworkType==='injected_network'} fullWidth className="mb-3"></TextField>
                                                    </div>
                                                </CardBody>
                                            </Card> : <></>
                                        }
                                        <div className="mb-3">
                                            <Label>Token</Label>
                                            <FormControl variant="filled" fullWidth style={{ marginBottom: "31px" }} required size="small">
                                                <InputLabel id="from-token">{"Select token"}</InputLabel>

                                                <Select labelId="from-token" onChange={handleFromTokenChange}>
                                                    {fromTokens.map(token => (
                                                        <MenuItem key={token.id} value={token.id}>
                                                        {token.token_name}
                                                        </MenuItem>
                                                    ))}
                                                </Select>
                                            </FormControl>
                                        </div>
                                        <div className="mb-5">
                                            <Label>Amount</Label>
                                            {/* <Form.Control type="number" value={amount} onChange={handleAmountChange}/> */}
                                            <TextField type="number" value={amount} onChange={handleAmountChange} fullWidth className="mb-3"></TextField>

                                            <p className="muted mt-2">Max amount: {maxAmount}</p>
                                        </div>

                                    </div>
                                    <div className="col col-5">
                                        <h5 className="text-center">To</h5>
                                        <div className="d-flex flex-row flex-wrap mb-1">
                                            <FormControl variant="filled" fullWidth style={{ marginBottom: "31px" }} required size="small">
                                                <InputLabel id="to-network-type">{"Select network type"}</InputLabel>

                                                <Select labelId="to-network-type" onChange={handleToNetworkTypeChange}>
                                                    <MenuItem value={"user_defined_network"}>{"Use user defined network"}</MenuItem>
                                                    <MenuItem value={"injected_network"}>{"Use injected Ethereum network"}</MenuItem>
                                                </Select>
                                            </FormControl>   
                                        </div>
                                        <div className="mb-3">
                                            <Label>Network</Label>
                                            <FormControl variant="filled" fullWidth style={{ marginBottom: "31px" }} required size="small">
                                                <InputLabel id="to-network">{"Select network"}</InputLabel>

                                                <Select labelId="to-network" onChange={handleToNetworkChange}>
                                                    {toNetworks.map(network => (
                                                        <MenuItem key={network.network_id} value={network.network_id}>
                                                        {network.name}
                                                        </MenuItem>
                                                    ))}
                                                </Select>
                                            </FormControl>
                                        </div>

                                        {toNetworkType==='user_defined_network'?
                                            <Card>
                                                <CardHeader>
                                                    Fabric credential
                                                </CardHeader>
                                                <CardBody>
                                                    <div className="mb-3">
                                                        <Label>Organization</Label>
                                                        <FormControl variant="filled" fullWidth style={{ marginBottom: "31px" }} required size="small" disabled={toNetworkType==='injected_network'}>
                                                            <InputLabel id="from-org">{"Select organization"}</InputLabel>

                                                            <Select labelId="from-org" onChange={handleMinterOrgChange}>
                                                                {minter_orgs.map(org => (
                                                                    <MenuItem key={org.name} value={org.name}>
                                                                    {org.name}
                                                                    </MenuItem>
                                                                ))}
                                                            </Select>
                                                        </FormControl>
                                                    </div>
                                                    <div className="mb-3">
                                                        <Label>Username</Label>
                                                        <TextField type="text" value={minter_username} onChange={handleMinterUsernameChange} disabled={toNetworkType==='injected_network'} fullWidth className="mb-3"></TextField>
                                                    </div>
                                                </CardBody>
                                            </Card> : <></>
                                        }

                                        <div className="mb-3">
                                            <Label>Token</Label>
                                            <FormControl variant="filled" fullWidth style={{ marginBottom: "31px" }} required size="small">
                                                <InputLabel id="to-token">{"Select token"}</InputLabel>

                                                <Select labelId="to-token" onChange={handleToTokenChange}>
                                                    {toTokens.map(token => (
                                                        <MenuItem key={token.id} value={token.id}>
                                                        {token.token_name}
                                                        </MenuItem>
                                                    ))}
                                                </Select>
                                            </FormControl>

                                        </div>
                                        <div className="mb-3">
                                            <Label>To Address</Label>
                                            <TextField type="text" value={toAddress} onChange={handleToAddressChange} disabled={toNetworkType==='user_defined_network'} fullWidth className="mb-3"></TextField>
                                        </div>

                                        
                                    </div>
                                </div>

                                <div className="d-flex justify-content-end align-items-center">
                                    <span className="text-danger mr-3">{errorMessage}</span>
                                    {loading && <Spinner animation="border" role="status">
                                        <span className="visually-hidden">Loading...</span>
                                    </Spinner>}
                                    <Button color='primary' onClick={handleSubmit} disabled={!isSubmittable()}>{transfering ? 'Tranfering...' : 'Transfer'}</Button>
                                </div>
                            </CardBody>
                        </Card>
                    </Col>
                </Row>
            </Container>
        </>
    )
}

export default TransferTokenPage