import { Paper } from "@material-ui/core";
import { DataGrid } from "@material-ui/data-grid";
import { useSnackbar } from "notistack";
import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { ERR_TOP_CENTER } from "../../../utils/snackbar-utils";
import { setPreloadCertDocuments } from "./redux";
import axios from "axios";
import { getUniversity, getUser } from "src/utils/mng_user";
import { makeStyles } from "@material-ui/core";

const useStyles = makeStyles((theme) => ({
    root: {
        "& .MuiDataGrid-root .MuiDataGrid-columnsContainer": {
            background: "#3f51b5",
            color: "white",
        },
    },
}));
const columns = [
    { field: "id", headerName: "STT", width: 85, type: "string" },
    { field: "studentId", headerName: "Mã số sv", width: 125, type: "string" },
    { field: "name", headerName: "Họ và tên", width: 200, type: "string" },
    { field: "faculty", headerName: "Ngành học", width: 200, type: "string" },
    { field: "cpa", headerName: "CPA", width: 80, type: "string" },
    { field: "level", headerName: "Xếp loại", width: 125, type: "string" },
    {
        field: "grad_year",
        headerName: "Năm tốt nghiệp",
        width: 125,
        type: "string",
    },
    {
        field: "eduform",
        headerName: "Hình thức đào tạo",
        width: 200,
        type: "string",
    },
    { field: "register_id", headerName: "Số hiệu", width: 200, type: "string" },
    { field: "status", headerName: "Trạng thái", width: 200, type: "string" },
    { field: "timestamp", headerName: "Ngay Cap", width: 200, type: "string" },
    { field: "txid", headerName: "Txid", width: 250, type: "string" },
];

export default function UploadedCertificateTable(props) {
    const cls = useStyles();
    const fetching = useSelector((state) => state.certificateSlice.fetching);
    const docs = useSelector((state) => state.certificateSlice.docs);
    const universityProfile = useSelector((state) => state.profileSlice);
    const university = getUniversity();
    let newestVersionCertificates = [];
    newestVersionCertificates = docs.map((doc, index) => {
        return {
            id: index + 1,
            studentId: doc.student_id,
            name: doc.student_name,
            faculty: doc.student_major,
            cpa: doc.cpa,
            level: doc.certificate_level,
            grad_year: doc.grad_year,
            eduform: doc.education_form,
            timestamp: doc.timestamp,
            status: doc.status,
            register_id: doc.register_id,
        };
    });

    const dp = useDispatch();
    const { enqueueSnackbar } = useSnackbar();

    useEffect(() => {
        fetchUploadedCertDocuments();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    async function fetchUploadedCertDocuments() {
        try {
            const response = await axios.get("/certificates/?university=" + (universityProfile.id || ""));
            dp(setPreloadCertDocuments(response.data));
        } catch (error) {
            console.error(error);
            if (error.response) enqueueSnackbar(JSON.stringify(error.response.data), ERR_TOP_CENTER);
        }
    }

    return (
        // newestVersionCertificates.length !== 0 && (
        <Paper className={cls.root} style={{ height: "600px", width: "100%" }}>
            {fetching ? null : <DataGrid rows={newestVersionCertificates} columns={columns} pageSize={10} rowsPerPageOptions={[5, 10, 20]} pagination rowHeight={48} loading={fetching} />}
        </Paper>
        // )
    );
}
