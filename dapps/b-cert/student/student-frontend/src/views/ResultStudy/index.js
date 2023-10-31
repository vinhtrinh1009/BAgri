import React, { Component, useEffect } from "react";
import { Grid, makeStyles, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from "@material-ui/core";
import { Paper } from "@material-ui/core";
import { DataGrid } from "@material-ui/data-grid";
import Page from "src/shared/Page";
import axios from "axios";
import { useSnackbar } from "notistack";
import { ERR_TOP_CENTER } from "src/utils/snackbar-utils";
import { useState } from "react";
import { useSelector } from "react-redux";

const useStyle = makeStyles((theme) => ({
    root: {
        "& > *": {
            marginBottom: theme.spacing(2),
            "&:last-child": {
                marginBottom: 0,
                boxShadow: "2px 2px 7px -1px",
            },
        },
        padding: theme.spacing(2.5),
    },
    data_Grid: {
        "& .MuiDataGrid-root": {
            border: "none",
        },
        "& .MuiDataGrid-root .MuiDataGrid-columnsContainer": {
            background: "#009688",
            color: "white",
            lineHeight: "50px",
            fontSize: "12px",
        },
    },
}));
const columns = [
    { field: "id", headerName: "#", width: 50, type: "string" },
    { field: "semester", headerName: "Học kỳ", width: 130, type: "string" },
    { field: "subject_code", headerName: "Mã Học Phần", width: 150, type: "string" },
    { field: "subject_name", headerName: "Tên Học Phần", width: 180, type: "string" },
    { field: "class_id", headerName: "Mã Lớp Học", width: 150, type: "string" },
    { field: "midScore", headerName: "Điểm QT", width: 150, type: "string" },
    { field: "finalScore", headerName: "Điểm CK", width: 150, type: "string" },
    { field: "wordScore", headerName: "Trạng thái", type: "string" },
];
export default function ResultStudy() {
    const cls = useStyle();
    const [state, setState] = useState({ data: [], loading: true });
    const student = useSelector((stores) => stores.studentProfileSlice);
    const { enqueueSnackbar } = useSnackbar();

    useEffect(() => {
        getdata();
    }, []);
    console.log("data", state);

    async function getdata() {
        try {
            const response = await axios.get("/results/?user=" + student.user.id);
            const data = response.data.map((data, index) => {
                return {
                    id: index + 1,
                    semester: data.class_detail.semester,
                    subject_code: data.class_detail.subject_id,
                    subject_name: data.class_detail.subject_name,
                    class_id: data.class_detail.class_id,
                    midScore: data.middle_score,
                    finalScore: data.final_score,
                    wordScore: data.middle_score == -1 || data.final_score == -1 ? "Chua nhap diem" : "",
                };
            });
            setState((prev) => {
                return {
                    ...prev,
                    data: data,
                    loading: false,
                };
            });
        } catch (error) {
            console.error(error);
            if (error.response) enqueueSnackbar(JSON.stringify(error.response.data), ERR_TOP_CENTER);
        }
    }

    return (
        <Page title="Kết quả học tập">
            <div className={cls.root}>
                <Paper className={cls.data_Grid} style={{ height: "600px", width: "100%" }}>
                    <TableContainer>
                        <Table sx={{ minWidth: 1300 }} aria-label="result study table">
                            <TableHead>
                                <TableRow>
                                    {columns.map((col, index) => {
                                        return <TableCell key={col.field}>{col.headerName}</TableCell>;
                                    })}
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {state.data.map((data, index) => {
                                    return (
                                        <TableRow key={data.finalScore + "-" + data.midScore + index}>
                                            <TableCell>{data.id}</TableCell>
                                            <TableCell>{data.semester}</TableCell>
                                            <TableCell>{data.subject_code}</TableCell>
                                            <TableCell>{data.subject_name}</TableCell>
                                            <TableCell>{data.class_id}</TableCell>
                                            <TableCell>{data.midScore}</TableCell>
                                            <TableCell>{data.finalScore}</TableCell>
                                            <TableCell>{data.wordScore}</TableCell>
                                        </TableRow>
                                    );
                                })}
                            </TableBody>
                        </Table>
                    </TableContainer>
                </Paper>
            </div>
        </Page>
    );
}
