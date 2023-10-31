import { Box, Divider, Grid, makeStyles, Paper, Table, TableBody, TableCell, TableContainer, TableRow, Typography, Button } from "@material-ui/core";

import axios from "axios";
import { useSnackbar } from "notistack";
import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router";
import { ERR_TOP_CENTER } from "../../utils/snackbar-utils";

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

export default function DecryptedCertInfo(props) {
    const { cert_txid } = props;
    const cls = useStyles();
    const { enqueueSnackbar } = useSnackbar();
    const [certificate, setCertificate] = useState({});

    useEffect(() => {
        fetchCertificateData();
    }, [cert_txid]);

    async function fetchCertificateData() {
        if (cert_txid != "") {
            try {
                const response = await axios.get("/get-certificate-data/" + cert_txid + "/");
                console.log("cert", response.data);
                setCertificate({
                    ...response.data[0].data,
                    link: response.data[0].link,
                    action: response.data[0].payload_decode.action,
                    timestamp: response.data[0].payload_decode.timestamp,
                    certificate: response.data[0].payload_decode[response.data[0].payload_decode.action.toLowerCase()],
                });
                try {
                } catch (error) {
                    enqueueSnackbar(JSON.stringify(error.response), ERR_TOP_CENTER);
                }
            } catch (error) {
                enqueueSnackbar(JSON.stringify(error.response), ERR_TOP_CENTER);
            }
        }
    }

    return (
        <>
            {certificate.link ? (
                <>
                    <Paper className={cls.root}>
                        <Box display="flex" alignItems="center" pt={2} pb={1}>
                            <Typography variant="h4" className={cls.typo}>
                                Thông tin bằng cấp
                            </Typography>
                        </Box>
                        <Divider style={{ marginBottom: "30px" }}></Divider>
                        <div style={{ width: "100%", overflow: "auto", paddingBottom: "20px" }}>
                            <Grid container spacing={2} style={{ width: "1267px" }}>
                                <Grid item xs={2}>
                                    University:
                                </Grid>
                                <Grid item xs={4}>
                                    <Typography>{certificate?.certificate?.university_university_id}</Typography>
                                </Grid>
                                <Grid item xs={6}>
                                    <Typography>
                                        <GetUniversityDataView university_id={certificate?.certificate?.university_university_id || 0} />
                                    </Typography>
                                </Grid>

                                <Grid item xs={2}>
                                    Student:
                                </Grid>
                                <Grid item xs={4}>
                                    <Typography>{certificate?.certificate?.student_student_id}</Typography>
                                </Grid>
                                <Grid item xs={6}>
                                    <Typography>
                                        <GetStudentDataView student_id={certificate?.certificate?.student_student_id || 0} />
                                    </Typography>
                                </Grid>

                                <Grid item xs={2}>
                                    CPA:
                                </Grid>
                                <Grid item xs={4}>
                                    {/* <Typography>{certificate?.certificate?.cpa}</Typography> */}
                                </Grid>
                                <Grid item xs={6}>
                                    <Typography>{certificate?.certificate?.cpa}</Typography>
                                </Grid>

                                <Grid item xs={2}>
                                    Loại bằng:
                                </Grid>
                                <Grid item xs={4}></Grid>
                                <Grid item xs={6}>
                                    <Typography>{certificate?.certificate?.type || ""}</Typography>
                                </Grid>
                                <Grid item xs={2}>
                                    Ngày cấp
                                </Grid>
                                <Grid item xs={4}></Grid>
                                <Grid item xs={6}>
                                    <Typography>{new Date(Number(certificate?.timestamp) * 1000).toLocaleString("it-IT") || ""}</Typography>
                                </Grid>
                                <Grid item xs={2}>
                                    Mã giao dịch
                                </Grid>
                                <Grid item xs={10}>
                                    <Typography style={{ overflow: "hidden", textOverflow: "ellipsis" }}>
                                        <a href={`${process.env.REACT_APP_EXPLORER_URL}/transactions/${cert_txid}`} style={{ color: "#4caf50" }}>
                                            {cert_txid || ""}
                                        </a>
                                    </Typography>
                                </Grid>
                            </Grid>
                        </div>
                    </Paper>
                </>
            ) : (
                <></>
            )}
        </>
    );
}

function GetUniversityDataView(props) {
    const { university_id } = props;
    const [name, setName] = useState("Decoding data...");
    useEffect(() => {
        if (university_id) {
            (async () => {
                try {
                    const response = await axios.get(`get-university-data/${university_id}/`);
                    console.log(response.data.data);
                    setName(response.data?.data?.university?.university_name || "");
                } catch (error) {
                    console.log(error.response);
                    setName("Decode error");
                }
            })();
        }
    }, [university_id]);
    return <>{name}</>;
}

function GetStudentDataView(props) {
    const { student_id } = props;
    const [name, setName] = useState("Decoding data...");
    useEffect(() => {
        if (student_id) {
            (async () => {
                try {
                    const response = await axios.get(`get-student-data/${student_id}/`);
                    console.log(response.data.data);
                    setName(response.data?.data?.student?.name || "");
                } catch (error) {
                    console.log(error.response);
                    setName("Decode error");
                }
            })();
        }
    }, [student_id]);
    return <>{name}</>;
}
