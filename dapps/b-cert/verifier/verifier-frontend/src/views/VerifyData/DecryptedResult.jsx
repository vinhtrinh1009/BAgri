import { Box, Divider, Grid, IconButton, makeStyles, Paper, Typography } from "@material-ui/core";
import axios from "axios";
import React, { useEffect, useLayoutEffect, useState } from "react";
import { Eye } from "react-feather";
import DialogTransaction from "./DialogTransaction";
const useStyles = makeStyles((theme) => ({
    root: {
        padding: theme.spacing(0, 2, 2, 2),
    },
    paper: {
        padding: theme.spacing(0, 2, 2, 2),
    },
    typo: {
        flexGrow: 1,
    },
}));
export default function DecryptedResult(props) {
    const { results_txid = [] } = props;
    const cls = useStyles();
    const [modalTranx, setModalTranx] = useState({ open: false, data: {} });
    function openModelTx(resultdata) {
        console.log(resultdata);
        setModalTranx({ open: true, data: resultdata });
    }
    return (
        <Paper style={{ padding: "15px" }}>
            <Box display="flex" alignItems="center" pt={2} pb={1}>
                <Typography variant="h4" className={cls.typo}>
                    Thông tin bảng điểm
                </Typography>
            </Box>
            <Divider style={{ marginBottom: "30px" }}></Divider>
            <div style={{ width: "100%", overflow: "auto", padding: "20px 0px" }}>
                <Grid container spacing={2} style={{ width: "1267px", fontSize: "12px", fontWeight: "bold" }}>
                    <Grid item xs={2}>
                        MSSV
                    </Grid>
                    <Grid item xs={2}>
                        Mã lớp
                    </Grid>
                    <Grid item xs={3}>
                        Tên môn học
                    </Grid>
                    <Grid item xs={1}>
                        Trọng số QT
                    </Grid>
                    <Grid item xs={1}>
                        Điểm QT
                    </Grid>
                    <Grid item xs={1}>
                        Điểm CK
                    </Grid>
                    <Grid item xs={2}>
                        Lịch sử điểm
                    </Grid>
                </Grid>
                <Divider style={{ margin: "15px 0px" }}></Divider>
                <Grid container spacing={2} style={{ width: "1267px" }}>
                    {results_txid.map((item, index) => {
                        return <ResultData txid={item} key={item + "-" + index} openModel={openModelTx}></ResultData>;
                    })}
                </Grid>
            </div>
            <DialogTransaction
                open={modalTranx.open}
                result_data={modalTranx.data}
                handle_close={() => {
                    setModalTranx((prev) => {
                        return { ...prev, open: false };
                    });
                }}
            />
        </Paper>
    );
}

function ResultData(props) {
    const { txid, openModel = () => {} } = props;
    const [data, setData] = useState({});

    function openModelTx(resultdata) {
        openModel(resultdata);
    }

    useLayoutEffect(() => {
        (async () => {
            try {
                const response = await axios.get(`get-result-data/${txid}/`);
                console.log(response.data[0]);
                setData({
                    ...response.data[0].data,
                    link: response.data[0].link,
                    action: response.data[0].payload_decode.action,
                    timestamp: response.data[0].payload_decode.timestamp,
                    result: response.data[0].payload_decode[response.data[0].payload_decode?.action?.toLowerCase()],
                });
            } catch (error) {
                console.log(error.response);
            }
        })();
    }, [txid]);
    return (
        <>
            <Grid item xs={2} style={{ display: "flex", alignItems: "center" }}>
                <Typography>{data.result?.student_student_id.split("-")[1]}</Typography>
            </Grid>
            <Grid item xs={2} style={{ display: "flex", alignItems: "center" }}>
                <Typography>{data.result?.classroom_class_id.split("-")[1]}</Typography>
            </Grid>
            <Grid item xs={3} style={{ display: "flex", alignItems: "center" }}>
                <Typography>
                    <DeCodeClassName id_class={data.result?.classroom_class_id} />
                </Typography>
            </Grid>
            <Grid item xs={1} style={{ display: "flex", alignItems: "center" }}>
                <Typography>{"0.3"}</Typography>
            </Grid>
            <Grid item xs={1} style={{ display: "flex", alignItems: "center" }}>
                <Typography>{data.result?.middlescore == -1 ? "---" : data.result?.middlescore}</Typography>
            </Grid>
            <Grid item xs={1} style={{ display: "flex", alignItems: "center" }}>
                <Typography>{data.result?.finallscore == -1 ? "---" : data.result?.finallscore}</Typography>
            </Grid>
            <Grid item xs={2} style={{ display: "flex", alignItems: "center" }}>
                <IconButton onClick={() => openModelTx(data)}>
                    <Eye width={16} height={16} />
                </IconButton>
            </Grid>
        </>
    );
}

function DeCodeClassName(props) {
    const { id_class } = props;
    const [name, setName] = useState("Decoding data...");
    useEffect(() => {
        if (id_class) {
            (async () => {
                try {
                    const response = await axios.get(`get-classroom-data/${id_class}/`);
                    try {
                        const response2 = await axios.get(`get-subject-data/${response.data?.data?.classroom?.subject_subject_id || 0}/`);
                        // console.log(response2.data.data);
                        setName(response2.data?.data?.subject?.subject_name || "");
                    } catch (error) {
                        console.log(error.response);
                        setName("Decode error");
                    }
                } catch (error) {
                    console.log(error.response);
                    setName("Decode error");
                }
            })();
        }
    }, [id_class]);
    return <>{name}</>;
}
