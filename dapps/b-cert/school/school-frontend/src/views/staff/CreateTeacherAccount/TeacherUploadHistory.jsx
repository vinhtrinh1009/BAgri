import { useEffect } from "react";
import { Accordion, makeStyles, Paper } from "@material-ui/core";
import { DataGrid } from "@material-ui/data-grid";
import { useDispatch, useSelector } from "react-redux";
// import { getToken } from "src/utils/mng-token";
import { setPreloadProfessors } from "./redux";
import { useSnackbar } from "notistack";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import SimpleTable from "../../../shared/Table/SimpleTable";
import GetAppIcon from "@material-ui/icons/GetApp";
import XLSX from "xlsx";
import { getLinkFromTxid } from "../../../utils/utils";
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
    { field: "id", headerName: "STT", width: 80, type: "string" },
    { field: "department", headerName: "Bộ môn", width: 85, type: "string" },
    { field: "professor_id", headerName: "Mã giảng viên", width: 125, type: "string" },
    { field: "name", headerName: "Họ và tên", width: 200, type: "string" },
    { field: "username", headerName: "Tên tài khoản", width: 200, type: "string" },
    { field: "email", headerName: "Email", width: 300, type: "string" },
    { field: "txid", headerName: "Txid", width: 125, type: "string" },
];

export default function TeacherUploadHistory() {
    const cls = useStyles();
    const fetching = useSelector((state) => state.teacherSlice.fetching);
    const reload_data = useSelector((state) => state.teacherSlice.reload_table);
    const professors = useSelector((state) => state.teacherSlice.professors);
    const universityProfile = useSelector((state) => state.profileSlice);
    const dp = useDispatch();
    const { enqueueSnackbar } = useSnackbar();

    useEffect(() => {
        fetchHistory();
    }, [reload_data]);

    async function fetchHistory() {
        try {
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/api/v1/professor/?university=${universityProfile.id || ""}`);
            const result = await response.data;
            dp(
                setPreloadProfessors(
                    result.map((professor, index) => {
                        return {
                            id: index + 1,
                            department: professor.department,
                            professor_id: professor.professor_id,
                            name: professor.user.full_name,
                            username: professor.user.username,
                            email: professor.user.email,
                        };
                    })
                )
            );
        } catch (error) {
            enqueueSnackbar(`${error}`, ERR_TOP_CENTER);
        }
    }
    const content = (
        <Paper className={cls.root} style={{ height: "600px", width: "100%" }}>
            {fetching ? null : <DataGrid rows={professors} columns={columns} pageSize={10} rowsPerPageOptions={[5, 10, 20]} pagination rowHeight={48} loading={fetching} />}
        </Paper>
    );
    return fetching ? null : content;
}
