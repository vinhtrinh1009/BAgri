import React, { useEffect } from "react";
import { Box, Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Grid, IconButton, makeStyles, Paper, Tab } from "@material-ui/core";
import { Alert, AlertTitle, TabContext, TabList, TabPanel } from "@material-ui/lab";
import { useSnackbar } from "notistack";
import { useState } from "react";
import { useSelector } from "react-redux";
import { getToken } from "../../../utils/mng-token";
import FileSaver from "file-saver";
import { ERR_TOP_CENTER, SUCCESS_TOP_CENTER } from "../../../utils/snackbar-utils";
import axios from "axios";
import { Trash2 } from "react-feather";
var QRCode = require("qrcode.react");

const useStyles = makeStyles((theme) => ({
    root: {
        padding: theme.spacing(2),
        "& .MuiTypography-gutterBottom": {
            marginBottom: 0,
        },
        "& .MuiAlert-message": {
            width: "100%",
            paddingRight: "30px",
        },
    },
}));

export default function BarForShareButton(props) {
    const cls = useStyles();
    const certificateData = useSelector((state) => state.shareCertificateSlice.certificateData);
    const [modelToken, setModelToken] = useState({ open: false, token_show: "" });
    const [tokenList, setTokenList] = useState([]);
    const { enqueueSnackbar } = useSnackbar();

    useEffect(() => {
        getListToken();
    }, []);
    async function getListToken() {
        try {
            (async () => {
                const res = await axios.get("/student/tokenize-certificate/");
                console.log(res.data);
                setTokenList(res.data);
            })();
        } catch (error) {
            console.log(error);
            enqueueSnackbar("Chưa có bằng cấp để chia sẻ!", ERR_TOP_CENTER);
        }
    }
    async function hdClick() {
        if (certificateData === []) {
            enqueueSnackbar("Chưa có bằng cấp để chia sẻ!", ERR_TOP_CENTER);
            return;
        }
        // supose backend already sort versions
        if (!certificateData.status) {
            enqueueSnackbar("Không thể chia sẻ bằng cấp đã bị thu hồi!", ERR_TOP_CENTER);
            return;
        }

        try {
            const response = await axios.post("/student/tokenize-certificate/", { certificate: certificateData.id });
            getListToken();
        } catch (error) {
            enqueueSnackbar(JSON.stringify(error.response), ERR_TOP_CENTER);
        }
    }

    async function deleteToken(token_id) {
        try {
            const res = await axios.delete("/student/tokenize-certificate/?tokenId=" + token_id);
            enqueueSnackbar("Delete success!", SUCCESS_TOP_CENTER);
            getListToken();
        } catch (error) {
            enqueueSnackbar("Delete fail!", ERR_TOP_CENTER);
        }
    }

    function checkTimeOut(created_date) {
        const time_remain = new Date(created_date) - Date.now() + 7 * 24 * 60 * 60 * 1000; // token co han trong 7 ngay
        console.log(time_remain);
        if (time_remain > 0) return true;
        else {
            return false;
        }
    }

    return (
        <Paper className={cls.root}>
            <Grid container spacing={3}>
                <Grid item xs={10}>
                    <Alert severity="success">
                        <AlertTitle>Bạn có thể chia sẻ bằng cấp </AlertTitle>
                    </Alert>
                </Grid>

                <Grid item xs={2} style={{ display: "flex", alignItems: "center", justifyContent: "space-around" }}>
                    <Button style={{ width: "100%" }} variant="contained" color="primary" onClick={hdClick} disabled={Boolean(!certificateData)}>
                        Tạo token
                    </Button>
                </Grid>
            </Grid>
            {tokenList.map((token, index) => {
                return (
                    <Grid container spacing={3} key={token.token}>
                        <Grid item xs={10}>
                            <Alert severity={checkTimeOut(token.created_at) ? "success" : "error"}>
                                <div style={{ width: "100%", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{token.token}</div>
                            </Alert>
                        </Grid>

                        <Grid item xs={2} style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                            <Button variant="contained" color="primary" onClick={() => setModelToken({ open: true, token_show: token.token })} disabled={Boolean(!certificateData)}>
                                Chia sẻ
                            </Button>
                            <IconButton variant="outlined" color="secondary" style={{ width: "fit-content" }} onClick={() => deleteToken(token.id)}>
                                <Trash2></Trash2>
                            </IconButton>
                        </Grid>
                    </Grid>
                );
            })}
            <TokenDialog
                open={modelToken.open}
                token={modelToken.token_show}
                closeModal={() => {
                    setModelToken({ open: false, token_show: "" });
                }}
            ></TokenDialog>
        </Paper>
    );
}

function TokenDialog({ open, token, closeModal }) {
    const [value, setValue] = React.useState("1");

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };
    function copy() {
        if (value == "1") {
            navigator.clipboard.writeText(token);
            closeModal();
        } else if (value == "2") {
            navigator.clipboard.writeText(`${process.env.REACT_APP_VERIFIER_URL}/ket-qua/${token}`);
            closeModal();
        } else if (value == "3") {
            const canvas = document.getElementById("qrcode");
            canvas.toBlob(function (blob) {
                // navigator.clipboard.write(blob);
            });
        }
    }
    function download_token() {
        if (value == "1") {
            var blob = new Blob([token], { type: "text/plain;charset=utf-8" });
            FileSaver.saveAs(blob, "BCertificate-Token.jwt");
            closeModal();
        } else if (value == "2") {
            var blob = new Blob([`${process.env.REACT_APP_VERIFIER_URL}/ket-qua/${token}`], { type: "text/plain;charset=utf-8" });
            FileSaver.saveAs(blob, "BCertificate-Link.jwt");
            closeModal();
        } else if (value == "3") {
            const canvas = document.getElementById("qrcode");
            canvas.toBlob(function (blob) {
                FileSaver.saveAs(blob, "BcertQRcode.png");
            });
        }
    }

    return (
        <Dialog open={open} onClose={(e) => closeModal()}>
            <DialogTitle>Chia se bang cap</DialogTitle>
            <DialogContent>
                <Box sx={{ width: "100%", typography: "body1" }}>
                    <TabContext value={value}>
                        <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
                            <TabList onChange={handleChange} aria-label="lab API tabs example">
                                <Tab label="Token" value="1" />
                                <Tab label="Link" value="2" />
                                <Tab label="QR code" value="3" />
                            </TabList>
                        </Box>
                        <TabPanel value="1">
                            <DialogContentText style={{ wordWrap: "break-word" }}>{token}</DialogContentText>
                        </TabPanel>
                        <TabPanel value="2">
                            <DialogContentText style={{ wordWrap: "break-word" }}>
                                <a href={`${process.env.REACT_APP_VERIFIER_URL}/ket-qua/${token}`} target="_blank">{`${process.env.REACT_APP_VERIFIER_URL}/ket-qua/${token}`}</a>
                            </DialogContentText>
                        </TabPanel>
                        <TabPanel value="3">
                            <div style={{ textAlign: "center" }}>
                                <QRCode includeMargin={true} level="L" id="qrcode" size={200} value={`${process.env.REACT_APP_VERIFIER_URL}/ket-qua/${token}`} />
                            </div>
                        </TabPanel>
                    </TabContext>
                </Box>
            </DialogContent>
            <DialogActions>
                <Button color="primary" onClick={copy} style={{ display: value == "3" ? "none" : "" }}>
                    Copy
                </Button>
                <Button color="primary" onClick={download_token}>
                    Download
                </Button>
            </DialogActions>
        </Dialog>
    );
}
