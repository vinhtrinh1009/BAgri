import React, { useEffect, useState, useLayoutEffect } from "react";
import { Row, Col, Container, Card, CardBody, Media } from "reactstrap";
import { useParams } from "react-router";
import { getTokenDetail, deleteToken, getContractCode, getContractInterface } from "src/services/User/tokens";
import LinkedTokensCard from "./components/LinkedTokensCard";
import { getBareToken } from "src/utils/token";
import DownloadIcon from "@mui/icons-material/Download";
import IconButton from "@mui/material/IconButton";
import Button from "@mui/material/Button";
import MuiAlert from "@mui/material/Alert";
import CodeMirror from "@uiw/react-codemirror";
import ZoomOutMapIcon from "@mui/icons-material/ZoomOutMap";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import { Box, Snackbar, Modal } from "@mui/material";
import { imagePath } from "../../../../constant/imagePath";
import { statusNetworkClassName } from "../../../../constant/statusNetworkClassName";
import { networkStatus } from "../../../../constant/networkStatus";
import { ScreenShare } from "@mui/icons-material";
import { Trash2 } from "react-feather";

const boxStyle = {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    width: "95%",
    maxHeight: "95%",
};

const Alert = React.forwardRef(function Alert(props, ref) {
    return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

const TokenDetailPage = () => {
    // const display_token = useSelector(state=>state.Token.display_token)
    const [display_token, setDisplayToken] = useState([]);
    const [loaded, setLoaded] = useState(false);
    const [contractCode, setContractCode] = useState("");
    const [contractInterface, setContractInterface] = useState("");
    const [openContractCode, setOpenContractCode] = useState(false);
    const [openContractInterface, setOpenContractInterface] = useState(false);
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const params = useParams();

    useLayoutEffect(() => {
        async function fetchData() {
            try {
                const response = await getTokenDetail({ token_type: params.token_type, token_id: params.tokenid });
                setDisplayToken(response.data);
                setLoaded(true);
                if (response.data.network) {
                    const response2 = await getContractCode({ url: response.data.contract_file });
                    const response3 = await getContractInterface({ url: response.data.abi });
                    setContractCode(response2.data);
                    setContractInterface(JSON.stringify(response3.data, null, 4));
                    console.log(response.data);
                }
            } catch (error) {
                alert("Something wrong happens!");
                console.log(error);
            }
        }
        fetchData();
    }, []);

    const handleRemoveToken = () => {
        deleteToken({ token_type: "fungible", id: display_token.id })
            .then((res) => {
                window.location = "/tokens";
            })
            .catch((e) => {
                alert("Unable to remove token");
            });
    };

    const handleCloseContractCode = () => {
        setOpenContractCode(false);
    };

    const handleCloseContractInterface = () => {
        setOpenContractInterface(false);
    };

    const handleOpenContractCode = () => {
        setOpenContractCode(true);
    };

    const handleOpenContractInterface = () => {
        setOpenContractInterface(true);
    };

    const handleCopyContractCode = () => {
        navigator.clipboard.writeText(contractCode);
        setOpenSnackbar(true);
    };

    const handleCopyContractInterface = () => {
        navigator.clipboard.writeText(contractInterface);
        setOpenSnackbar(true);
    };

    const handleCloseSnackbar = (event, reason) => {
        if (reason === "clickaway") {
            return;
        }

        setOpenSnackbar(false);
    };

    return (
        <>
            <Container style={{ maxWidth: "1605px", margin: "0 auto" }}>
                <div style={{ padding: "30px 0px" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "end" }}>
                        <h5 style={{ display: "flex", alignItems: "center", margin: 0 }}>
                            <div className="avatars mr-3">
                                <div className="avatar">
                                    <Media
                                        body
                                        className="img-60 rounded-circle"
                                        src={display_token?.token_icon || imagePath.TOKEN_DEFAULT}
                                        alt="#"
                                        onError={(e) => {
                                            e.currentTarget.src = imagePath.TOKEN_DEFAULT;
                                        }}
                                    />
                                </div>
                            </div>
                            <div style={{ textTransform: "capitalize" }}>
                                {display_token?.token_name || "Loading..."}
                                <div className="state">
                                    <div
                                        className={`dot-notify ${
                                            display_token.status == "Success"
                                                ? statusNetworkClassName.CREATED
                                                : display_token.status == "Pending"
                                                ? statusNetworkClassName.CREATE_PENDING
                                                : statusNetworkClassName.CREATE_FAIL
                                        }`}
                                    ></div>
                                    <div style={{ opacity: "0.5" }}>{display_token.status}</div>
                                </div>
                            </div>
                        </h5>
                        <div className="text-right">
                            <Button href={display_token.sdk + `&token=${getBareToken()}`} variant="outlined" style={{ marginRight: "10px" }}>
                                <DownloadIcon width={17} style={{ marginRight: "5px" }} /> SDK
                            </Button>
                            <Button variant="contained" color="primary" onClick={handleRemoveToken}>
                                <Trash2 width={17} style={{ marginRight: "5px" }} /> Remove
                            </Button>
                        </div>
                    </div>
                </div>
                <Card>
                    <CardBody style={{ padding: "30px" }}>
                        <h6 style={{ color: "#8CB8D8" }}>BASIC INFORMATION</h6>
                        <br />
                        <Row>
                            <Col className="col-md-4">
                                <div className="mb-1" style={{ opacity: "0.65" }}>
                                    Name
                                </div>
                                <strong>{display_token.token_name}</strong>
                            </Col>
                            <Col className="col-md-4">
                                <div className="mb-1" style={{ opacity: "0.65" }}>
                                    Symbol
                                </div>
                                <strong>{display_token.token_symbol}</strong>
                            </Col>
                            <Col className="col-md-4">
                                <div className="mb-1" style={{ opacity: "0.65" }}>
                                    Token Standard
                                </div>
                                <strong>{display_token.token_standard}</strong>
                            </Col>
                            {display_token.user_defined_network ? (
                                <Col className="col-md-4 mt-3">
                                    <div className="mb-1" style={{ opacity: "0.65" }}>
                                        Fabric network ID
                                    </div>
                                    <strong style={{ width: "100%" }}>{display_token.user_defined_network}</strong>
                                </Col>
                            ) : (
                                <Col className="col-md-4 mt-3">
                                    <div className="mb-1" style={{ opacity: "0.65" }}>
                                        Address
                                    </div>
                                    <strong style={{ width: "100%" }}>{display_token.address ? display_token.address : <span className="text-muted">Not deployed</span>}</strong>
                                </Col>
                            )}
                            {/* <Col className="col-md-4 mt-3">
                                <div className="mb-1" style={{ opacity: "0.65" }}>
                                    Address
                                </div>

                                <strong style={{ width: "100%" }}>{display_token.address ? display_token.address : <span className="text-muted">Not deployed</span>}</strong>
                            </Col> */}

                            <Col className="col-md-4 mt-3">
                                <div className="mb-1" style={{ opacity: "0.65" }}>
                                    Status
                                </div>
                                <strong>{display_token.status}</strong>
                            </Col>
                        </Row>

                        {contractCode && contractInterface && (
                            <>
                                <br />
                                <hr />
                                <div className="d-flex flex-row justify-content-between align-items-center my-1">
                                    <h6 className="mb-3" style={{ color: "#8CB8D8", textTransform: "uppercase" }}>
                                        Contract Code
                                    </h6>

                                    <div>
                                        <Button className="mr-1" variant="contained" size="small" href={display_token.contract_file} target="_blank">
                                            Export Code
                                        </Button>
                                        <IconButton className="mr-1" size="small" variant="contained" onClick={handleCopyContractCode}>
                                            <ContentCopyIcon />
                                        </IconButton>
                                        <IconButton size="small" variant="contained" onClick={handleOpenContractCode}>
                                            <ZoomOutMapIcon />
                                        </IconButton>
                                        {/* <Button variant='contained' size='small' startIcon={<ZoomOutMapIcon/>}></Button> */}
                                    </div>
                                </div>
                                <CodeMirror
                                    value={contractCode}
                                    height="400px"
                                    editable={false}
                                    // extensions={[javascript({ jsx: true })]}

                                    style={{ border: "1px solid lightgray", borderRadius: "8px", overflow: "hidden" }}
                                    className="mb-5"
                                />
                                <div className="d-flex flex-row justify-content-between align-items-center my-1">
                                    <h6 className="mb-3" style={{ color: "#8CB8D8", textTransform: "uppercase" }}>
                                        Contract ABI
                                    </h6>

                                    <div>
                                        <Button className="mr-1" variant="contained" size="small" href={display_token.abi} target="_blank">
                                            Export ABI
                                        </Button>
                                        <IconButton className="mr-1" size="small" variant="contained" onClick={handleCopyContractInterface}>
                                            <ContentCopyIcon />
                                        </IconButton>
                                        <IconButton size="small" variant="contained" onClick={handleOpenContractInterface}>
                                            <ZoomOutMapIcon />
                                        </IconButton>
                                        {/* <Button variant='contained' size='small' startIcon={<ZoomOutMapIcon/>}></Button> */}
                                    </div>
                                </div>
                                <CodeMirror
                                    value={contractInterface}
                                    height="400px"
                                    editable={false}
                                    // extensions={[javascript({ jsx: true })]}

                                    style={{ border: "1px solid lightgray", borderRadius: "8px", overflow: "hidden" }}
                                />
                            </>
                        )}
                    </CardBody>
                </Card>
            </Container>

            <Modal open={openContractCode} onClose={handleCloseContractCode} aria-labelledby="modal-modal-title" aria-describedby="modal-modal-description">
                <Box style={boxStyle}>
                    <CodeMirror value={contractCode} height="800px" editable={false} style={{ border: "1px solid lightgray", borderRadius: "8px", overflow: "hidden" }} className="mb-5" />
                </Box>
            </Modal>

            <Modal open={openContractInterface} onClose={handleCloseContractInterface} aria-labelledby="modal-modal-title" aria-describedby="modal-modal-description">
                <Box style={boxStyle}>
                    <CodeMirror value={contractInterface} height="800px" editable={false} style={{ border: "1px solid lightgray", borderRadius: "8px", overflow: "hidden" }} className="mb-5" />
                </Box>
            </Modal>

            <Snackbar open={openSnackbar} autoHideDuration={1500} onClose={handleCloseSnackbar} anchorOrigin={{ vertical: "top", horizontal: "center" }}>
                <Alert onClose={handleCloseSnackbar} severity="success" sx={{ width: "100%" }}>
                    Copied to clipboard !
                </Alert>
            </Snackbar>
        </>
    );
};

export default TokenDetailPage;
