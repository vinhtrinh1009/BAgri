import React, { useState, useEffect, useRef } from "react";
import { Badge } from "react-bootstrap";
import { updateToken } from "src/services/User/tokens";
import { LoadingButton } from '@mui/lab';
import Web3 from 'web3';
import { getContractBinary, getContractInterface, createFabricToken } from "../../../../../services/User/tokens";
import { Col, Row } from "reactstrap";

export default function Step2(props) {
    // const [enableSubmit, setEnableSubmit] = useState(true);
    // const [loading, setLoading] = useState(false);
    const [deploying, setDeploying] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");

    // const [network, setNetwork] = useState(undefined);
    const [connected, setConnected] = useState(false);
    const [contract, setContract] = useState({});

    // const [connecting, setConnecting] = useState(false);

    const [account, setAccount] = useState(undefined);

    const web3Ref = useRef(undefined);

    const [contractBinary, setContractBinary] = useState(undefined);
    const [contractInterface, setContractInterface] = useState(undefined);

    async function handleSubmit2() {
        props.onDataChange({ ...props.data, contract: { ...contract, address: "asdfasd" } });
        props.jumpToStep(3);
    }

    async function handleSubmit(){
        if(props.data.network.type === 'injected_network'){
            const accounts = await web3Ref.current.eth.getAccounts();

            // console.log("Attempting to deploy from account", accounts[0]);
            console.log('binary', contractBinary.length);
            console.log('interface', contractInterface.length);
    
            console.log(contractInterface);
            console.log(contract);
    
            setDeploying(true);
    
            for(let i=2; i<contract.arguments.length; i++){
                contract.arguments[i] = new web3Ref.current.utils.BN(contract.arguments[i]).mul(new web3Ref.current.utils.BN(10).pow(new web3Ref.current.utils.BN(contract.decimal)));
            
                console.log('args: ', contract.arguments[i].toString());
            }
    
            try{
                const deployingContract = await new web3Ref.current.eth.Contract(contractInterface);
                const deployedContract = await deployingContract.deploy({data: contractBinary, arguments: contract.arguments}).send({from: accounts[0]});
                
                console.log(deployedContract);
                console.log(deployedContract.address, deployedContract._address, deployedContract.options.address)
    
                setDeploying(false);
    
                props.onDataChange({...props.data, contract: {...contract, address: deployedContract._address ? deployedContract._address : deployedContract.options.address}});
                props.jumpToStep(3);
                
            } catch(error){
                if(error.code === 4001){
                    setDeploying(false);
                    return;
                }
    
                console.error(error);
                alert(error.message ? error.messsage : "Something wrong happens. Please try again.");
                props.jumpToStep(0)
            }
        } else if (props.data.network.type === 'user_defined_network'){
            createFabricToken(contract).then(res => {
                    props.onDataChange({...props.data, contract: res.data});
                    props.jumpToStep(3);
                }).catch(error => {
                    console.error(error);
                    alert(error.message ? error.messsage : "Something wrong happens. Please try again.");
                    props.jumpToStep(0)
                })
        }

        // const accounts = await web3Ref.current.eth.getAccounts();

        // // console.log("Attempting to deploy from account", accounts[0]);
        // console.log('binary', contractBinary.length);
        // console.log('interface', contractInterface.length);

        // console.log(contractInterface);
        // console.log(contract);

        // setDeploying(true);

        // for(let i=2; i<contract.arguments.length; i++){
        //     contract.arguments[i] = new web3Ref.current.utils.BN(contract.arguments[i]).mul(new web3Ref.current.utils.BN(10).pow(new web3Ref.current.utils.BN(contract.decimal)));
        
        //     console.log('args: ', contract.arguments[i].toString());
        // }

        // try{
        //     const deployingContract = await new web3Ref.current.eth.Contract(contractInterface);
        //     const deployedContract = await deployingContract.deploy({data: contractBinary, arguments: contract.arguments}).send({from: accounts[0]});
            
        //     console.log(deployedContract);
        //     console.log(deployedContract.address, deployedContract._address, deployedContract.options.address)

        //     setDeploying(false);

        //     props.onDataChange({...props.data, contract: {...contract, address: deployedContract._address ? deployedContract._address : deployedContract.options.address}});
        //     props.jumpToStep(3);
            
        // } catch(error){
        //     if(error.code === 4001){
        //         setDeploying(false);
        //         return;
        //     }

        //     console.error(error);
        //     alert(error.message ? error.messsage : "Something wrong happens. Please try again.");
        //     props.jumpToStep(0)
        // }

        // const result = await new web3Ref.current.eth.Contract(contractInterface)
        //     .deploy({data: contractBinary, arguments: contract.arguments})
        //     .send({ gas: "10000000", gasPrice: "5000000000", from: accounts[0] });

        // setDeploying(false);

        // console.log("Contract deployed to", result.options.address);

        // props.onDataChange({...props.data, contract: {...contract, address: result.options.address}});
        // props.jumpToStep(2);
    }

    useEffect(() => {
        let valid = true;
        if (!connected) valid = false;

        // setEnableSubmit(valid);
    }, [connected]);

    useEffect(() => {
        if (props.data.contract) {
            setContract(props.data.contract);

            // updateToken({
            //     token_type: ['ERC-20', 'ERC-721'].includes(props.data.contract.token_standard) ? 'fungible' : 'non_fungible',
            //     id: props.data.contract.id,
            //     address: props.data.contract.address,
            //     network: props.data.network.name
            // }).catch(e => {
            //     alert("Something wrong happens. Please try again.")
            // })
        } else setContract({});
    }, [props.data]);

    useEffect(() => {
        if (!contract || !contract.compiled_code) return;

        if (!contractBinary) {
            getContractBinary({ url: contract.compiled_code })
                .then((res) => {
                    setContractBinary(res.data);
                })
                .catch((err) => {
                    alert(err.message ? err.message : "Something wrong happened. Please reload the page.");
                });
        }
        if (!contractInterface) {
            getContractInterface({ url: contract.abi })
                .then((res) => {
                    setContractInterface(res.data);
                })
                .catch((err) => {
                    alert(err.message ? err.message : "Something wrong happened. Please reload the page.");
                });
        }
    }, [contract]);

    useEffect(() => {
        if (props.data.network.type === "injected_network") {
            window.ethereum.request({ method: "eth_requestAccounts" }).then((res) => {
                web3Ref.current = new Web3(window.ethereum);

                web3Ref.current.eth.getAccounts().then((res) => {
                    setAccount(res[0]);
                });
            });

            console.log("Use injected_network");
        } else if (props.data.network.type === "user_defined_network") {
            console.log("Use user_defined_network");
        }
    }, []);

    const truncateAccountAddress = (addr) => {
        if (!addr) return addr;
        return addr.substr(0, 5) + "..." + addr.substr(38, 3);
    };

    return (
        <div className="container step_3">
            <div className="d-flex justify-content-center w-100 flex-column align-items-center">
                <div className="mb-3">
                    <h5>A new token is ready to be deployed</h5>
                    <Row className="setup_info">
                        <Col md={6}>
                            <span>Name:</span>
                        </Col>
                        <Col md={6}>
                            <span>{contract.token_name}</span>
                        </Col>
                    </Row>
                    <Row className="setup_info">
                        <Col md={6}>
                            <span>Symbol:</span>
                        </Col>
                        <Col md={6}>
                            <span>{contract.token_symbol}</span>
                        </Col>
                    </Row>
                    <Row className="setup_info">
                        <Col md={6}>
                            <span>Standard:</span>
                        </Col>
                        <Col md={6}>
                            <span>{contract.token_standard}</span>
                        </Col>
                    </Row>
                </div>
                {props.data.network_type === "injected_network" && <Badge pill bg="success">{`Connected to ${account ? truncateAccountAddress(account) : "undefined"}`}</Badge>}
            </div>

            <div className="d-flex justify-content-center align-items-center">
                <span className="text-danger mr-3">{errorMessage}</span>
                <LoadingButton
                    variant="contained"
                    onClick={handleSubmit}
                    disabled={deploying}
                    loading={deploying}
                    style={deploying ? { minWidth: "150px" } : { minWidth: "100px" }}
                    disableElevation={true}
                >
                    {deploying ? "Deploying..." : "Deploy"}
                </LoadingButton>
            </div>
        </div>
    );
}
