import React, { useEffect, useState } from "react";
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Grid, Typography, IconButton } from "@material-ui/core";
import axios from "axios";
import { useSnackbar } from "notistack";
import { ERR_TOP_CENTER } from "../../utils/snackbar-utils";
import { useParams } from "react-router";

export default function DialogTransaction(props) {
    const { open = false, handle_close = () => {}, result_data = {} } = props;
    const { enqueueSnackbar } = useSnackbar();
    const { token } = useParams();
    const [blockData, setBlockData] = useState([]);
    const handleClose = () => {
        handle_close();
    };
    useEffect(() => {
        if (open == true) {
            const datapost = { result_id: result_data.result?.result_id, token: token };
            (async () => {
                try {
                    const response = await axios.post(`${process.env.REACT_APP_SCHOOL_BACKEND_URL}/api/v1/employee_view_history_of_result/`, datapost);
                    console.log(response.data);
                    setBlockData(response.data.data);
                } catch (error) {
                    console.error(error);
                    enqueueSnackbar("Load detail transaction fail!", ERR_TOP_CENTER);
                }
            })();
        }
    }, [open]);
    function fillterdata(score) {
        return isNaN(parseFloat(score)) || parseFloat(score) < 0 ? "---" : score;
    }
    return (
        <Dialog open={open} onClose={handleClose} fullWidth maxWidth="lg">
            <DialogTitle style={{ fontSize: "18px" }}>
                Lịch sử điểm: sinh viên: {result_data.result?.student_student_id.split("-")[1]} - mã lớp: {result_data.result?.classroom_class_id.split("-")[1]}
            </DialogTitle>
            <DialogContent style={{ minHeight: "50vh", padding: "25px" }}>
                <Grid container spacing={2} style={{ marginBottom: "20px" }}>
                    <Grid item xs={1}>
                        <Typography style={{ fontWeight: "bold" }}>STT</Typography>
                    </Grid>
                    <Grid item xs={2}>
                        <Typography style={{ fontWeight: "bold" }}>Mã giao dịch</Typography>
                    </Grid>
                    <Grid item xs={2}>
                        <Typography style={{ fontWeight: "bold" }}>Thời gian tạo</Typography>
                    </Grid>
                    <Grid item xs={3}>
                        <Typography style={{ fontWeight: "bold" }}>Người tạo</Typography>
                    </Grid>
                    <Grid item xs={2}>
                        <Typography style={{ fontWeight: "bold" }}>Kiểu</Typography>
                    </Grid>
                    <Grid item xs={1}>
                        <Typography style={{ fontWeight: "bold" }}>Điểm GK</Typography>
                    </Grid>
                    <Grid item xs={1}>
                        <Typography style={{ fontWeight: "bold" }}>Điểm CK</Typography>
                    </Grid>
                </Grid>
                {blockData.map((item, index) => {
                    return (
                        <Grid container spacing={3} key={"tran" + item.tx_data.data.header_signature}>
                            <Grid item xs={1}>
                                <Typography>{index + 1}</Typography>
                            </Grid>
                            <Grid item xs={2}>
                                <a href={`${process.env.REACT_APP_EXPLORER_URL}/transactions/${item.tx_data.data.header_signature}`} target="_blank">
                                    <Typography style={{ width: "100%", overflow: "hidden", textOverflow: "ellipsis" }}>{item.tx_data.data.header_signature}</Typography>
                                </a>
                            </Grid>
                            <Grid item xs={2}>
                                <Typography>{new Date(Number(item.tx_data.payload_decode.timestamp) * 1000).toLocaleString("it-IT")}</Typography>
                            </Grid>
                            <Grid item xs={3}>
                                <Typography>{item.signer.name}</Typography>
                            </Grid>
                            <Grid item xs={2}>
                                <Typography>{item.tx_data.payload_decode.action || "CREATE"}</Typography>
                            </Grid>
                            <Grid item xs={1}>
                                <Typography>{fillterdata(item.tx_data.payload_decode[item.tx_data.payload_decode.action.toLowerCase()].middlescore)}</Typography>
                            </Grid>
                            <Grid item xs={1}>
                                <Typography>{fillterdata(item.tx_data.payload_decode[item.tx_data.payload_decode.action.toLowerCase()].finallscore)}</Typography>
                            </Grid>
                        </Grid>
                    );
                })}
            </DialogContent>
            <DialogActions>
                <Button onClick={handleClose}>Close</Button>
            </DialogActions>
        </Dialog>
    );
}
