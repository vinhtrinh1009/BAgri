import React, { useEffect, useState, useRef } from "react";
import { Button, FormControl, InputLabel, Select, ListSubheader, MenuItem } from "@mui/material";
import Web3 from "web3";
import { getFabricNetworks, getEtherNetworks } from "src/services/User/tokens";

export default function Step0(props) {
    const [network, setNetwork] = useState({ id: 0, type: "" });
    const [connectingState, setConnectingState] = useState(0);
    const [etherNetworks, setEtherNetworks] = useState([]);
    const [fabricNetworks, setFabricNetworks] = useState([]);

    useEffect(() => {
        getFabricNetworks().then((res) => {
            for (let i = 0; i < res.data.length; i++) {
                res.data[i].type = "user_defined_network";
                // res.data[i].id = res.data[i].chain_id;
            }
            setFabricNetworks(res.data);
        });

        getEtherNetworks().then((res) => {
            let data = [];
            for (let i = 0; i < res.data.length; i++) {
                if (!res.data[i].supported) continue;
                data.push({ ...res.data[i], id: res.data[i].chain_id, type: "injected_network" });
            }
            setEtherNetworks(data);
        });
    }, []);

    const [account, setAccount] = useState(undefined);

    const [enableSubmit, setEnableSubmit] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");
    const [warningMessage, setWarningMessage] = useState("");
    const [loading, setLoading] = useState(false);

    const web3Ref = useRef(undefined);

    const handleNetworkChange = (e) => {
        setNetwork(e.target.value);
    };

    useEffect(async () => {
        if (network.type === "injected_network") {
            // check if network is valid
            if (!network.supported) {
                setConnectingState(0);
                setErrorMessage("We have not support this network yet.");
                return;
            } else setErrorMessage("");

            // check if MetaMask is installed
            if (!window.ethereum) {
                alert("MetaMask is not installed.");
                return;
            }

            setConnectingState(1);
            setLoading(true);
            setEnableSubmit(false);

            try {
                await window.ethereum.request({
                    method: "wallet_switchEthereumChain",
                    params: [{ chainId: `0x${network.id.toString(16)}` }], // chainId must be in hexadecimal numbers
                });
            } catch (e) {
                if (e.code === 4001) {
                    // User rejected the request.
                    setNetwork({ id: "", type: "" });
                }
                return;
            }

            try {
                const addresses = await window.ethereum.request({ method: "eth_requestAccounts" });
                if (addresses.length === 0) throw "Unable to get accounts";
                setAccount(addresses[0]);
            } catch (e) {
                if (e.code === 4001) {
                    // User rejected the request.
                    setNetwork({ id: "", type: "" });
                }
                return;
            }

            web3Ref.current = new Web3(window.ethereum);
            setConnectingState(2);
            setLoading(false);
            setEnableSubmit(true);

            window.ethereum.on("accountsChanged", (accounts) => {
                console.log("accountsChanged");

                if (accounts.length > 0) {
                    setAccount(accounts[0]);
                    setConnectingState(2);
                } else {
                    // disconnect
                    setNetwork({ id: "", type: "" });
                    setConnectingState(0);
                    setAccount(undefined);
                    setEnableSubmit(false);
                }
            });

            window.ethereum.on("networkChanged", (networkId) => {
                // Time to reload your interface with the new networkId
                const nid = parseInt(networkId);

                let chosenNetwork = undefined;
                for (let i = 0; i < etherNetworks.length; i++) {
                    if (nid === etherNetworks[i].id && etherNetworks[i].supported) {
                        chosenNetwork = etherNetworks[i];
                        break;
                    }
                }

                if (!chosenNetwork) {
                    setNetwork({ supported: false, type: "" });
                    setEnableSubmit(false);
                    setConnectingState(0);
                    setErrorMessage("We have not support this network yet.");
                } else setNetwork(chosenNetwork);
            });
        } else if (network.type === "user_defined_network") {
            // setNetwork({id: '', type: network.type});
            setConnectingState(0);
            setAccount(undefined);
            web3Ref.current = undefined;

            setEnableSubmit(true);
        }
    }, [network]);

    const connectingText = (state) => {
        switch (state) {
            case 0:
                return "";
            case 1:
                return "Connecting to Wallet...";
            case 2:
                return `Connected to ${account ? truncateAccountAddress(account) : "undefined"}`;
            default:
                return "Undefined state";
        }
    };

    const handleSubmit = (e) => {
        if (!enableSubmit) {
            alert("Form is invalid. Please check again before continue.");
            return;
        }
        props.onDataChange({ ...props.data, network: network });
        props.jumpToStep(1);
    };

    const truncateAccountAddress = (addr) => {
        if (!addr) return addr;
        return addr.substr(0, 5) + "..." + addr.substr(38, 4);
    };

    return (
        <div className="container" style={{ textAlign: "center" }}>
            <FormControl fullWidth margin="normal" size="small" variant="filled" style={{ maxWidth: "500px" }}>
                <InputLabel>Select Network</InputLabel>
                <Select value={network} id="grouped-select" label="Network" onChange={handleNetworkChange}>
                    <ListSubheader>Ethereum</ListSubheader>
                    {etherNetworks.map((network, i) => (
                        <MenuItem key={i} value={network}>
                            {network.name}
                        </MenuItem>
                    ))}

                    <ListSubheader>Hyperledger Fabric</ListSubheader>
                    {fabricNetworks.map((network, i) => (
                        <MenuItem key={i} value={network}>
                            {network.name}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
            <div className="d-flex justify-content-center align-items-center mt-3">
                <span>{connectingText(connectingState)}</span>

                <div className="d-flex justify-content-end align-items-center">
                    {errorMessage ? <span className="text-danger mr-3">{errorMessage}</span> : <span className="text-warning mr-3">{warningMessage}</span>}
                    <Button variant="contained" style={{ minWidth: "100px" }} onClick={handleSubmit} disabled={!enableSubmit}>
                        Next
                    </Button>
                </div>
            </div>
        </div>
    );
}
