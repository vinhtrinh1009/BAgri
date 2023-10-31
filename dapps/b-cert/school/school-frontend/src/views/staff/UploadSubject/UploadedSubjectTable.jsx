import { Paper } from "@material-ui/core";
import { DataGrid } from "@material-ui/data-grid";
import { useSnackbar } from "notistack";
import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import axios from "axios";
import { getUniversity } from "src/utils/mng_user";
import { getToken } from "../../../utils/mng-token";
import { setPreloadSubjects } from "./redux";
import { makeStyles } from "@material-ui/core";
import { ERR_TOP_CENTER } from "../../../utils/snackbar-utils";

const columns = [
    { field: "id", headerName: "#", width: 100, type: "string" },
    { field: "subject_id", headerName: "Mã môn học", width: 155, type: "string" },
    { field: "name", headerName: "Tên môn học", width: 400, type: "string" },
    { field: "credits", headerName: "Số tín chỉ", width: 200, type: "number" },
];

const useStyles = makeStyles((theme) => ({
    root: {
        backgroundColor: "white",
    },
}));

export default function UploadedSubjectTable(props) {
    const cls = useStyles();
    const fetching = useSelector((state) => state.subjectSlice.fetching);
    const reload_table = useSelector((state) => state.subjectSlice.reload_table);
    const subjects = useSelector((state) => state.subjectSlice.subjects);
    const dp = useDispatch();
    const { enqueueSnackbar } = useSnackbar();
    const universityProfile = useSelector((state) => state.profileSlice);

    useEffect(() => {
        fetchUploadedSubject();
    }, [reload_table]);

    async function fetchUploadedSubject() {
        try {
            const response = await axios.get("subject/?university=" + (universityProfile.id || ""));
            dp(
                setPreloadSubjects(
                    response.data.map((subject, index) => {
                        return {
                            id: index + 1,
                            subject_id: subject.subject_id,
                            name: subject.name,
                            credits: subject.credits,
                        };
                    })
                )
            );
        } catch (error) {
            console.error(error);
            if (error.response) enqueueSnackbar(JSON.stringify(error.response.data), ERR_TOP_CENTER);
        }
    }

    return (
        <Paper className={cls.root} style={{ height: "350px", width: "100%" }}>
            <DataGrid
                loading={fetching}
                rows={subjects}
                columns={columns}
                rowHeight={48}
                autoPageSize
                pageSize={10}
                // autoHeight
                // rowsPerPageOptions={[5, 10, 25, 50, 100]}
            />
        </Paper>
    );
}
