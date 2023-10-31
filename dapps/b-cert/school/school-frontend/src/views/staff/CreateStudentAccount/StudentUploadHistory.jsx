import { Accordion, makeStyles, Paper } from "@material-ui/core";
import { DataGrid } from "@material-ui/data-grid";
import { useSnackbar } from "notistack";
import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getToken } from "src/utils/mng-token";
import SimpleTable from "../../../shared/Table/SimpleTable";
import { setPreloadStudents } from "./redux";
import GetAppIcon from "@material-ui/icons/GetApp";
import XLSX from "xlsx";
import { ERR_TOP_CENTER } from "../../../utils/snackbar-utils";
import axios from "axios";
import { getUniversity } from "src/utils/mng_user";

const useStyles = makeStyles((theme) => ({
    root: {
        width: "100%",
    },
    heading: {
        fontSize: theme.typography.pxToRem(15),
        fontWeight: theme.typography.fontWeightRegular,
    },
}));
const columns = [
    { field: "id", headerName: "STT", width: 60, type: "string" },
    { field: "student_id", headerName: "MSSV", width: 105, type: "string" },
    { field: "name", headerName: "Họ và tên", width: 200, type: "string" },
    { field: "email", headerName: "Email", width: 300, type: "string" },
    { field: "unit", headerName: "Đơn vị lớp", width: 150, type: "string" },
    { field: "major", headerName: "Ngành học", width: 150, type: "string" },
    { field: "education_form", headerName: "Hình thức đào tạo", width: 200, type: "string" },
    { field: "txid", headerName: "Txid", width: 125, type: "string" },
];
export default function StudentUploadHistory() {
    const cls = useStyles();
    const fetching = useSelector((state) => state.studentSlice.fetching);
    const reload_table = useSelector((state) => state.studentSlice.reload_table);
    const students = useSelector((state) => state.studentSlice.students);
    const universityProfile = useSelector((state) => state.profileSlice);
    const dp = useDispatch();
    const { enqueueSnackbar } = useSnackbar();

    useEffect(() => {
        fetchHistory();
    }, [reload_table]);

    async function fetchHistory() {
        try {
            const response = await axios.get("student/?university=" + (universityProfile.id || ""));
            dp(
                setPreloadStudents(
                    response.data.map((student, index) => {
                        return {
                            id: index + 1,
                            student_id: student.student_id,
                            name: student.user.full_name,
                            email: student.user.email,
                            unit: student.unit,
                            major: student.major,
                            education_form: student.education_form,
                        };
                    })
                )
            );
        } catch (error) {
            console.error(error);
            if (error.response) enqueueSnackbar(JSON.stringify(error.response.data), ERR_TOP_CENTER);
        }
    }

    const content = (
        <Paper className={cls.root} style={{ height: "600px", width: "100%" }}>
            {fetching ? null : <DataGrid rows={students} columns={columns} pageSize={10} rowsPerPageOptions={[5, 10, 20]} pagination rowHeight={48} loading={fetching} />}
        </Paper>
    );
    return fetching ? null : content;
}
