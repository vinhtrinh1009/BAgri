import {
    Accordion,
    AccordionActions,
    AccordionDetails,
    AccordionSummary,
    Box,
    Button,
    makeStyles,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    TextField,
    Typography,
} from "@material-ui/core";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import SaveIcon from "@material-ui/icons/Save";
import SendIcon from "@material-ui/icons/Send";
import { Timeline, TimelineConnector, TimelineContent, TimelineDot, TimelineItem, TimelineSeparator } from "@material-ui/lab";
import axios from "axios";
import { useSnackbar } from "notistack";
import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import AskOTP from "../../../layouts/TeacherDashboardLayout/AskOTP";
import Page from "../../../shared/Page";
import { requirePrivateKeyHex } from "../../../utils/keyholder";
import { isEnable2FA } from "../../../utils/mng-2fa";
import { ERR_TOP_CENTER, SUCCESS_BOTTOM_RIGHT, SUCCESS_TOP_CENTER } from "../../../utils/snackbar-utils";
import { getLinkFromTxid } from "../../../utils/utils";
import DialogTransaction from "./DialogTransaction";

const useStyles = makeStyles((theme) => ({
    root: {
        paddingLeft: 0,
        "& .MuiTimelineItem-missingOppositeContent:before": {
            flex: 0,
            padding: 0,
        },
        "& .MuiInputBase-input": {
            paddingLeft: "20px",
        },
        "& .MuiInputBase-input.Mui-disabled": {
            color: "black",
        },
        "& .MuiAccordion-root.Mui-expanded": {
            boxShadow: "0px 0px 8px -3px",
        },
    },

    accordionHeader: {
        alignItems: "center",
        justifyContent: "space-between",
    },
}));

export default function SubmitGrade(props) {
    const cls = useStyles();
    const [fetching, setFetching] = useState(true);
    const [results, setResults] = useState({});
    const [dataShow, setDataShow] = useState({});
    const professor_id = useSelector((state) => state.teacherProfileSlice.user.id);
    const [txModel, setTxModel] = useState({ open: false, tx_id: "" });
    const { enqueueSnackbar } = useSnackbar();

    useEffect(() => {
        fetchMyClasses();
    }, []);
    function openModelTx(txId) {
        setTxModel({ open: true, tx_id: txId });
    }
    async function fetchMyClasses() {
        try {
            const response = await axios.get("/classes/?professor=" + professor_id);
            // console.log("fetchgetClass", response.data);
            setFetching(false);
            let data_show = {};
            response.data.map((item, index) => {
                if (data_show[item.semester]) {
                    data_show[item.semester].push(item);
                } else {
                    data_show[item.semester] = [item];
                }
            });
            setDataShow(data_show);
        } catch (error) {
            console.error(error);
            if (error.response) enqueueSnackbar(JSON.stringify(error.response.data), ERR_TOP_CENTER);
        }
    }
    async function DongBoDiemQLDT(class_id, class_code) {
        enqueueSnackbar("Wait for fetching data!", SUCCESS_TOP_CENTER);
        try {
            const res = await axios.post(`http://dev.hust-edu.appspot.com/api/grades?accessKey=CJ2qNIdRNU7YuXQPTOGA-LamDB&classId=${class_code}`);
            const qldt_data = res.data.data;
            const leng_data = qldt_data.length;
            // let new_result_data = [...results[class_id]];

            setResults((prev) => {
                return {
                    ...prev,
                    [class_id]: prev[class_id].map((kq, index) => {
                        for (let i = 0; i < leng_data; i++) {
                            if (qldt_data[i].studentId == kq.student.student_id) {
                                if (qldt_data[i].status == -2) {
                                    // console.log("co thay ket qua", kq.student.student_id, "chua len diem");

                                    return {
                                        ...kq,
                                        middle_score: "",
                                        final_score: "",
                                    };
                                } else {
                                    console.log("co thay ket qua", kq.student.student_id, "da len diem");
                                    return {
                                        ...kq,
                                        middle_score: qldt_data[i].grade,
                                        is_edit_midScore: false,
                                        final_score: "",
                                    };
                                }
                            }
                        }
                        return {
                            ...kq,
                            middle_score: "",
                            final_score: "",
                        };
                    }),
                };
            });
            enqueueSnackbar("Sync success!", SUCCESS_TOP_CENTER);
        } catch (error) {
            enqueueSnackbar("Sync failed!", ERR_TOP_CENTER);
        }
    }
    async function getResultofClass(classId) {
        try {
            const response = await axios.get("results/?class=" + classId);
            setResults({
                ...results,
                [classId]: response.data.map((item, index) => {
                    return {
                        ...item.result,
                        transaction: item.transaction,
                        middle_score: fillterdata(item.result.middle_score),
                        final_score: fillterdata(item.result.final_score),
                    };
                }),
            });
            console.log(results);
        } catch (err) {
            enqueueSnackbar("Error get results study!", ERR_TOP_CENTER);
        }
    }
    function change_middle_score(class_id, result_id, score) {
        setResults((prev) => {
            return {
                ...prev,
                [class_id]: prev[class_id].map((item, index) => {
                    if (item.result_id == result_id) {
                        return {
                            ...item,
                            middle_score: fillterdata(score),
                        };
                    }
                    return item;
                }),
            };
        });
    }
    function fillterdata(score) {
        return isNaN(parseFloat(score)) || parseFloat(score) < 0 ? "" : score;
    }
    function change_final_score(class_id, result_id, score) {
        setResults((prev) => {
            return {
                ...prev,
                [class_id]: prev[class_id].map((item, index) => {
                    if (item.result_id == result_id) {
                        return {
                            ...item,
                            final_score: fillterdata(score),
                        };
                    }
                    return item;
                }),
            };
        });
    }
    async function submitUpdateResult(class_id) {
        enqueueSnackbar("Wait for updating!", SUCCESS_TOP_CENTER);
        try {
            const res = await axios.post("update-results/", results[class_id]);
            console.log(res.data);
            enqueueSnackbar("Update success!", SUCCESS_TOP_CENTER);
        } catch (error) {
            enqueueSnackbar("Update fail!", SUCCESS_TOP_CENTER);
            console.log(error);
        }
    }

    return (
        <Page title="Nhập điểm lớp học">
            {fetching ? null : (
                <>
                    {Object.keys(dataShow).length === 0 ? (
                        "Không tìm thấy lớp học nào!"
                    ) : (
                        <>
                            <Timeline className={cls.root}>
                                {Object.keys(dataShow).map((semeter, index) => {
                                    return (
                                        <TimelineItem key={semeter + "hoc_ki" + index}>
                                            <TimelineSeparator>
                                                <TimelineDot color="primary" />
                                                <TimelineConnector />
                                            </TimelineSeparator>
                                            <TimelineContent>
                                                <Box>
                                                    <Typography gutterBottom variant="h5">{`Kì ${semeter}`}</Typography>
                                                    <Box px={1}>
                                                        {dataShow[semeter].map((class_data, jindex) => {
                                                            return (
                                                                <Accordion
                                                                    key={"classinfo" + class_data.id + jindex}
                                                                    onChange={(e) => (e.target.className.includes("Mui-expanded") ? null : getResultofClass(class_data.id))}
                                                                >
                                                                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                                                                        {`Mã Lớp: ${class_data.class_id} | Mã học phần: ${class_data.subject_id} | ${class_data.subject_name}`}
                                                                    </AccordionSummary>
                                                                    <AccordionDetails>
                                                                        <TableContainer>
                                                                            <Typography style={{ textAlign: "right" }}>
                                                                                <Button variant="contained" color="primary" onClick={() => DongBoDiemQLDT(class_data.id, class_data.class_id)}>
                                                                                    Đồng Bộ qldt
                                                                                </Button>
                                                                            </Typography>
                                                                            <Table size="small">
                                                                                <TableHead>
                                                                                    <TableRow>
                                                                                        <TableCell>STT</TableCell>
                                                                                        <TableCell>MSSV</TableCell>
                                                                                        <TableCell>Họ và tên</TableCell>
                                                                                        {/* <TableCell>Ngày sinh</TableCell> */}
                                                                                        <TableCell>Email</TableCell>
                                                                                        <TableCell style={{ width: "100px" }}>Điểm GK</TableCell>
                                                                                        <TableCell style={{ width: "100px" }}>Điểm CK</TableCell>
                                                                                        {class_data.status && <TableCell style={{ width: "100px" }}>Txid</TableCell>}
                                                                                    </TableRow>
                                                                                </TableHead>
                                                                                <TableBody>
                                                                                    {results[class_data.id]?.map((student, index) => {
                                                                                        return (
                                                                                            <TableRow key={"resultImg" + class_data.id + student.id + index}>
                                                                                                <TableCell>{index + 1}</TableCell>
                                                                                                <TableCell>{student.student.student_id}</TableCell>
                                                                                                <TableCell>{student.student.user.last_name + " " + student.student.user.first_name}</TableCell>
                                                                                                {/* <TableCell>{student.birthday}</TableCell> */}
                                                                                                <TableCell>{student.student.user.email}</TableCell>
                                                                                                <TableCell>
                                                                                                    <TextField
                                                                                                        // type="number"
                                                                                                        value={student.middle_score}
                                                                                                        onChange={(e) => change_middle_score(class_data.id, student.result_id, e.target.value)}
                                                                                                        // error={!parseFloat(student.middle_score)}
                                                                                                        // helperText={halfError && "Từ 0 - 10"}
                                                                                                        disabled={student.is_edit_midScore == false}
                                                                                                    ></TextField>
                                                                                                </TableCell>
                                                                                                <TableCell>
                                                                                                    <TextField
                                                                                                        // type="number"
                                                                                                        value={student.final_score}
                                                                                                        onChange={(e) => change_final_score(class_data.id, student.result_id, e.target.value)}
                                                                                                        // error={finalError}
                                                                                                        disabled={fetching}
                                                                                                    ></TextField>
                                                                                                </TableCell>
                                                                                                <TableCell>
                                                                                                    <div
                                                                                                        style={{
                                                                                                            width: "100px",
                                                                                                            overflow: "hidden",
                                                                                                            textOverflow: "ellipsis",
                                                                                                            cursor: "pointer",
                                                                                                            display: student.transaction?.transaction_type == 2 ? "" : "none",
                                                                                                        }}
                                                                                                        onClick={() => openModelTx(student.transaction?.transaction_id)}
                                                                                                    >
                                                                                                        {student.transaction?.transaction_id}
                                                                                                    </div>
                                                                                                </TableCell>
                                                                                            </TableRow>
                                                                                        );
                                                                                    })}
                                                                                </TableBody>
                                                                            </Table>
                                                                        </TableContainer>
                                                                    </AccordionDetails>
                                                                    <AccordionActions style={{ justifyContent: "right", padding: "15px" }}>
                                                                        {/* <Typography>Note: "NAN" or "-1" value that means "Giao vien chua len diem"</Typography> */}
                                                                        <Button
                                                                            startIcon={<SendIcon></SendIcon>}
                                                                            variant="contained"
                                                                            color="primary"
                                                                            onClick={(e) => submitUpdateResult(class_data.id)}
                                                                            // disabled={disable}
                                                                        >
                                                                            Gửi điểm
                                                                        </Button>
                                                                    </AccordionActions>
                                                                </Accordion>
                                                            );
                                                        })}
                                                    </Box>
                                                </Box>
                                            </TimelineContent>
                                        </TimelineItem>
                                    );
                                })}
                            </Timeline>
                        </>
                    )}
                </>
            )}
            <DialogTransaction
                open={txModel.open}
                handle_close={() =>
                    setTxModel((prev) => {
                        return { ...prev, open: false };
                    })
                }
                tx_id={txModel.tx_id}
            />
        </Page>
    );
}
