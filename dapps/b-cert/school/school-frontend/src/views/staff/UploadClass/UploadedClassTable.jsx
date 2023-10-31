import { Paper, Box } from "@material-ui/core";
import SimpleTable from "../../../shared/Table/SimpleTable";
import { DataGrid } from "@material-ui/data-grid";
import { makeStyles } from "@material-ui/core";
import { useSnackbar } from "notistack";
import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getToken } from "../../../utils/mng-token";
import { ERR_TOP_CENTER } from "../../../utils/snackbar-utils";
import { getLinkFromTxid } from "../../../utils/utils";
import { setPreloadClasses } from "./redux";
import axios from "axios";
import { getUniversity } from "src/utils/mng_user";

const columns = [
    { field: "id", headerName: "#", width: 70, type: "string" },
    { field: "semester", headerName: "Kì học", width: 90, type: "string" },
    { field: "class_id", headerName: "Mã lớp học", width: 125, type: "string" },
    { field: "subject_id", headerName: "Mã môn học", width: 129, type: "string" },
    { field: "subject_name", headerName: "Tên môn học", width: 220, type: "string" },
    { field: "professor_id", headerName: "Mã GV", width: 125, type: "string" },
    { field: "professor_name", headerName: "GV", width: 180, type: "string" },
    { field: "student_list", headerName: "DSSV", width: 320, type: "string" },
];

const useStyles = makeStyles((theme) => ({
    root: {
        backgroundColor: "white",
    },
}));
export default function UploadedClassTable(props) {
    const cls = useStyles();
    const fetching = useSelector((state) => state.classSlice.fetching);
    const reload_table = useSelector((state) => state.classSlice.reload_table);
    const classes = useSelector((state) => state.classSlice.classes);
    const dp = useDispatch();
    const { enqueueSnackbar } = useSnackbar();
    const universityProfile = useSelector((state) => state.profileSlice);
    const university = getUniversity();

    useEffect(() => {
        fetchUploadedClass();
    }, [reload_table]);

    async function fetchUploadedClass() {
        try {
            const response = await axios.get("classes/?university=" + (universityProfile.id || ""));
            dp(setPreloadClasses(response.data));
        } catch (error) {
            console.error(error);
            if (error.response) enqueueSnackbar(JSON.stringify(error.response.data), ERR_TOP_CENTER);
        }
    }
    const content = (
        <Paper style={{ height: "350px", width: "100%" }}>
            <DataGrid
                className={cls.root}
                loading={fetching}
                rows={classes}
                columns={columns}
                rowHeight={48}
                autoPageSize
                // pageSize={5}
                // autoHeight
                // rowsPerPageOptions={[5, 10, 25, 50, 100]}
            />
        </Paper>
    );
    return fetching ? null : content;
}
