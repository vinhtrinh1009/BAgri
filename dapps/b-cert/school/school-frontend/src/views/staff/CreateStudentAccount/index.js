import { makeStyles } from "@material-ui/core";
import { useSnackbar } from "notistack";
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import DragnDropZone from "../../../shared/DragnDropZone";
import Page from "src/shared/Page";
import { getToken } from "src/utils/mng-token";
import StudentDataExample from "./StudentDataExample";
import StudentUploadHistory from "./StudentUploadHistory";
import { startUploadFile, uploadFileFail, uploadFileSuccess } from "./redux";
import axios from "axios";
import { getUniversity } from "src/utils/mng_user";
import { ERR_TOP_CENTER, SUCCESS_BOTTOM_CENTER, SUCCESS_TOP_CENTER } from "../../../utils/snackbar-utils";

const useStyles = makeStyles((theme) => ({
    root: {
        "& > *": {
            marginBottom: theme.spacing(2),
            "&:last-child": {
                marginBottom: 0,
            },
        },
        paddingBottom: theme.spacing(2.5),
    },
}));

export default function CreateStudentAccount() {
    const cls = useStyles();
    const uploading = useSelector((state) => state.studentSlice.uploading);
    const dp = useDispatch();
    const { enqueueSnackbar } = useSnackbar();
    const university = getUniversity();

    async function hdUploadFile(files) {
        dp(startUploadFile());
        const formData = new FormData();
        formData.append("excel-file", files[0]);
        formData.append("university", university);
        try {
            const response = await axios.post("/create-student/", formData);
            enqueueSnackbar("Tạo tài khoản sinh viên thành công!", SUCCESS_TOP_CENTER);
            dp(uploadFileSuccess());
        } catch (error) {
            dp(uploadFileFail());
            console.error(error);
            if (error.response) enqueueSnackbar(JSON.stringify(error.response.data), ERR_TOP_CENTER);
        }
    }

    return (
        <Page title="Tạo tài khoản sinh viên">
            <div className={cls.root}>
                <StudentDataExample></StudentDataExample>
                <DragnDropZone onDropAccepted={hdUploadFile} uploading={uploading}></DragnDropZone>
                <StudentUploadHistory></StudentUploadHistory>
            </div>
        </Page>
    );
}
