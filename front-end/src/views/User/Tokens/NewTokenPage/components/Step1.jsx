import React, { useEffect, useState, useRef } from "react";
import { Label, Media } from "reactstrap";
import { HelpCircle } from "react-feather";
import { TextField, Button, Stack, Checkbox, FormControlLabel } from "@mui/material";
import { LoadingButton } from "@mui/lab";
// import Web3 from 'web3';
import avatar_placeholder from "../../../../../assets/images/user/7.jpg";
import { createToken } from "../../../../../services/User/tokens";
import { createFabricToken } from "src/services/User/tokens";
import { useDispatch } from "react-redux";
import { OPEN_WARNING_ALERT } from "../../../../../redux/User/Alerts/actionTypes";

const DEFAULT_DECIMAL = 18;
const DEFAULT_INITIAL_SUPPLY = 1000;

export default function Step1(props) {
    const dispatch = useDispatch();
    const [tokenStandard, setTokenStandard] = useState("ERC-20");
    const [name, setName] = useState("");
    const [symbol, setSymbol] = useState("");
    // const [account, setAccount] = useState(undefined);

    const [iconUrl, setIconUrl] = useState(undefined);

    const [initialSupply, setInitialSupply] = useState(1000);
    const [decimal, setDecimal] = useState(18);
    const [maxSupply, setMaxSupply] = useState(1000000);

    const [burnable, setBurnable] = useState(true);
    const [pausable, setPausable] = useState(true);
    const [mintable, setMintable] = useState(true);

    const [enableSubmit, setEnableSubmit] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");
    const [loading, setLoading] = useState(false);

    const iconInputRef = useRef();
    // const web3Ref = useRef(undefined);
    // console.log(props.data.network);

    const handleTokenStandardChange = (value) => {
        setTokenStandard(value);
    };

    const handleNameChange = (e) => {
        setName(e.target.value);
    };

    const handleSymbolChange = (e) => {
        setSymbol(e.target.value.toUpperCase());
    };

    const handleInitialSupplyChange = (e) => {
        const newValue = e.target.value ? parseInt(e.target.value) : "";
        setInitialSupply(newValue);
    };

    const handleDecimalChange = (e) => {
        const newValue = e.target.value ? parseInt(e.target.value) : undefined;
        setDecimal(newValue);
    };

    const handleMaxSupplyChange = (e) => {
        const newValue = e.target.value;
        setMaxSupply(newValue);
    };

    const readUrl = (event) => {
        if (event.target.files.length === 0) return;
        if (event.target.files[0].size > 512000) {
            dispatch({ type: OPEN_WARNING_ALERT, payload: { message: "Image too large! Only accept size image smaller than 500KB" } });
            return;
        }
        console.log(event.target.files[0]);
        var mimeType = event.target.files[0].type;

        if (mimeType.match(/image\/*/) == null) return;

        var reader = new FileReader();
        reader.readAsDataURL(event.target.files[0]);
        reader.onload = (_event) => {
            setIconUrl(reader.result);
        };
    };

    const handleBurnableChange = (e) => {
        setBurnable(e.target.checked);
    };

    const handlePausableChange = (e) => {
        setPausable(e.target.checked);
    };

    const handleMintableChange = (e) => {
        setMintable(e.target.checked);

        console.log(e.target.checked);
    };

    const handleSubmit = (e) => {
        if (!enableSubmit) {
            alert("Form is invalid. Please check again before continue.");
            return;
        }
        setLoading(true);
        if (props.data.network.type === "injected_network") {
            createToken({
                token_type: ["ERC-20", "ERC-721"].includes(tokenStandard) ? "fungible" : "non_fungible",
                token_name: name,
                token_symbol: symbol,
                token_standard: tokenStandard,
                token_icon: iconInputRef.current.files[0] || undefined,
                decimal: decimal === undefined ? DEFAULT_DECIMAL : decimal,
                max_supply: maxSupply === undefined ? undefined : maxSupply,
                initial_supply: initialSupply === "" ? DEFAULT_INITIAL_SUPPLY : initialSupply,
                burnable: burnable,
                pausable: pausable,
                mintable: mintable,
                network: props.data.network.name,
            })
                .then((res) => {
                    props.onDataChange({ ...props.data, contract: res.data });
                    props.jumpToStep(2);
                })
                .catch((err) => {
                    alert("Something wrong happens. Please try again.");
                    setLoading(false);
                });
        }
        if (props.data.network.type === 'user_defined_network'){
            props.onDataChange({...props.data, contract: {
                token_type: ['ERC-20', 'ERC-721'].includes(tokenStandard) ? 'fungible' : 'non_fungible',
                token_name: name,
                token_symbol: symbol,
                token_standard: tokenStandard,
                token_icon: iconInputRef.current.files[0] || undefined,
                decimal: decimal === undefined ? DEFAULT_DECIMAL : decimal,
                max_supply: maxSupply === undefined ? undefined : maxSupply,
                initial_supply: initialSupply === undefined ? DEFAULT_INITIAL_SUPPLY : initialSupply,
                burnable: burnable,
                pausable: pausable,
                mintable: mintable,
                network: props.data.network.network_id,
            }})
            props.jumpToStep(2)
            // createFabricToken({
            //     token_type: ['ERC-20', 'ERC-721'].includes(tokenStandard) ? 'fungible' : 'non_fungible',
            //     token_name: name,
            //     token_symbol: symbol,
            //     token_standard: tokenStandard,
            //     token_icon: iconInputRef.current.files[0] || undefined,
            //     decimal: decimal === undefined ? DEFAULT_DECIMAL : decimal,
            //     max_supply: maxSupply === undefined ? undefined : maxSupply,
            //     initial_supply: initialSupply === undefined ? DEFAULT_INITIAL_SUPPLY : initialSupply,
            //     burnable: burnable,
            //     pausable: pausable,
            //     mintable: mintable,
            //     network: props.data.network.network_id,
            // }).then(res => {
            //     props.onDataChange({...props.data, contract: res.data});
            //     props.jumpToStep(3);
            // }).catch(err => {
            //     alert("Something wrong happens. Please try again.");
            //     setLoading(false);
            // })
        }
    };

    useEffect(() => {
        let isValid = true;
        if (name.trim().length === 0) {
            isValid = false;
            setErrorMessage("");
        } else if (name.trim().length > 64) {
            isValid = false;
            setErrorMessage("Name is too long (more than 64 characters)");
        } else if (symbol.trim().length === 0) {
            isValid = false;
            setErrorMessage("");
        } else if (symbol.trim().length > 64) {
            isValid = false;
            setErrorMessage("Symbol is too long (more than 64 characters");
        } else if (decimal !== undefined && (decimal < 0 || decimal > 32768)) {
            isValid = false;
            setErrorMessage("Decimal is not valid");
        } else if (initialSupply !== undefined && initialSupply < 0) {
            isValid = false;
            setErrorMessage("Initial supply is not valid");
        }

        setEnableSubmit(isValid);
        if (isValid) setErrorMessage("");
    }, [name, symbol, initialSupply, decimal, maxSupply, burnable, pausable, mintable, tokenStandard]);

    const handleAvatarClick = (e) => {
        iconInputRef.current.click();
    };

    return (
        <div className="container dapp_step1">
            <div className="row">
                <div className="col-md-3 col-12" style={{ display: "flex", alignItems: "center" }}>
                    <div className="d-flex flex-fill justify-content-center mb-5 dapp_img_wrapper" style={{ alignItems: "center" }}>
                        <div className="avata_wrapper">
                            <div className="avata_upload bg_upload">
                                <div>
                                    <div className="file_image_icon">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="49.558" height="57.818" viewBox="0 0 49.558 57.818">
                                            <path
                                                id="Icon_metro-file-image"
                                                data-name="Icon metro-file-image"
                                                d="M49.935,14.464a7.508,7.508,0,0,1,1.549,2.452,7.446,7.446,0,0,1,.645,2.839V56.924a3.085,3.085,0,0,1-3.1,3.1H5.668a2.987,2.987,0,0,1-2.194-.9,2.987,2.987,0,0,1-.9-2.194V5.3a2.987,2.987,0,0,1,.9-2.194,2.987,2.987,0,0,1,2.194-.9H34.577a7.448,7.448,0,0,1,2.839.645A7.508,7.508,0,0,1,39.869,4.4ZM35.61,6.591V18.723H47.741a3.525,3.525,0,0,0-.71-1.323L36.932,7.3a3.524,3.524,0,0,0-1.323-.71ZM48,55.892V22.853H34.577a3.085,3.085,0,0,1-3.1-3.1V6.333H6.7V55.892H48Zm-4.13-14.455V51.762H10.83V45.567l6.195-6.195,4.13,4.13,12.39-12.39ZM17.025,35.242a6.169,6.169,0,0,1-6.195-6.195,6.169,6.169,0,0,1,6.195-6.195,6.169,6.169,0,0,1,6.195,6.195,6.169,6.169,0,0,1-6.195,6.195Z"
                                                transform="translate(-2.571 -2.203)"
                                                fill="#b7ccdb"
                                            />
                                        </svg>
                                    </div>
                                    <div style={{ padding: "0px 40px", color: "#6C6C6C" }}>Drop an image here or click</div>
                                </div>
                            </div>
                            <div className="avata_upload img_uploaded" style={{ display: iconUrl ? "" : "none" }}>
                                <img src={iconUrl || avatar_placeholder} style={{ width: "inherit", height: "inherit", objectFit: "cover" }} />
                            </div>
                            <input ref={iconInputRef} onChange={(e) => readUrl(e)} className="avata_upload" type="file" id="drop_zone" />
                        </div>
                        {/* <div>
                            <Label>Icon</Label>
                            <div className="d-flex flex-row flex-grow-0">
                                <Media className="rounded-circle p-0" body alt="" src={iconUrl ? iconUrl : avatar_placeholder} style={{width: '150px', height: '150px', maxWidth: '150px', maxHeight: '150px'}} onClick={handleAvatarClick}/>
                                <input ref={iconInputRef} className="upload display-none" type="file" onChange={(e) => readUrl(e)}/>                            
                            </div>
                        </div> */}
                    </div>
                </div>

                <div className="col-md-9 col-12">
                    <Label>Token Standard</Label>
                    <Stack direction="row" spacing={1}>
                        <Button variant={tokenStandard === "ERC-20" ? "contained" : "outlined"} className="px-2 mb-2 mr-2 text-nowrap" onClick={() => handleTokenStandardChange("ERC-20")}>
                            <span style={tokenStandard === "ERC-20" ? { color: "white" } : {}}>ERC-20</span>
                        </Button>
                        {/* <Button variant={tokenStandard === 'ERC-721' ? 'contained' : 'outlined'}  className="px-2 mb-2 mr-2 text-nowrap" onClick={() => handleTokenStandardChange('ERC-721')} disabled><span style={tokenStandard === 'ERC-721' ? {color: 'white'} : {}}>ERC-721</span></Button> */}
                        {/* <Button variant={tokenStandard === 'ERC-777' ? 'contained' : 'outlined'}  className="px-2 mb-2 mr-2 text-nowrap" onClick={() => handleTokenStandardChange('ERC-777')} disabled><span style={tokenStandard === 'ERC-777' ? {color: 'white'} : {}}>ERC-777</span></Button> */}
                        {/* <Button variant={tokenStandard === 'ERC-1155' ? 'contained' : 'outlined'}  className="px-2 mb-2 mr-2 text-nowrap" onClick={() => handleTokenStandardChange('ERC-1155')} disabled><span style={tokenStandard === 'ERC-1155' ? {color: 'white'} : {}}>ERC-1155</span></Button> */}
                    </Stack>

                    <div className="row mt-3">
                        <div className="col col-md-6">
                            {/* <Label>Name*</Label> */}
                            <TextField label="Name" value={name} onChange={handleNameChange} variant="filled" fullWidth className="mb-4"></TextField>

                            {/* <Label>Symbol*</Label> */}
                            <TextField label="Symbol" value={symbol} onChange={handleSymbolChange} variant="filled" fullWidth className="mb-4"></TextField>

                            <div className="d-flex flex-row justify-content-between">
                                {/* <Label>Initial Supply*</Label> */}
                                {/* <span data-toggle='tooltip' title=''><HelpCircle width="12px"/></span>     */}
                            </div>

                            <TextField label="Initial Supply" variant="filled" type="number" value={initialSupply} onChange={handleInitialSupplyChange} fullWidth className="mb-4" />
                        </div>
                        <div className="col col-md-6">
                            <div className="d-flex flex-row justify-content-between">
                                {/* <Label>Max Supply</Label> */}
                                {/* <span data-toggle='tooltip' title='Leave blank for no capped supply'><HelpCircle width="12px"/></span>     */}
                            </div>
                            <TextField label="Max Supply" variant="filled" type="number" value={maxSupply} onChange={handleMaxSupplyChange} fullWidth className="mb-4"></TextField>

                            <div className="d-flex flex-row justify-content-between">
                                {/* <Label>Decimal*</Label> */}
                                {/* <span data-toggle='tooltip' title=''><HelpCircle width="12px"/></span>     */}
                            </div>
                            <TextField label="Decimal" variant="filled" type="number" value={decimal} onChange={handleDecimalChange} fullWidth className="mb-4" />

                            <Label>Extensions</Label>
                            <div>
                                <FormControlLabel
                                    disabled={props.data.network.type === "user_defined_network"}
                                    control={<Checkbox checked={mintable} onChange={handleMintableChange} />}
                                    label="Mintable"
                                />
                                <FormControlLabel
                                    disabled={props.data.network.type === "user_defined_network"}
                                    control={<Checkbox checked={pausable} onChange={handlePausableChange} />}
                                    label="Pausable"
                                />
                                <FormControlLabel
                                    disabled={props.data.network.type === "user_defined_network"}
                                    control={<Checkbox checked={burnable} onChange={handleBurnableChange} />}
                                    label="Burnable"
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div className="d-flex justify-content-center align-items-center mt-3">
                <span className="text-danger mr-3">{errorMessage}</span>
                <LoadingButton variant="contained" onClick={handleSubmit} disabled={!enableSubmit} style={{ minWidth: "100px" }} loading={loading} disableElevation={true}>
                    Next
                </LoadingButton>
            </div>
        </div>
    );
}
