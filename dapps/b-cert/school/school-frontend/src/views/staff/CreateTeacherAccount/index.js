import { makeStyles } from "@material-ui/core";
import axios from "axios";
import { useSnackbar } from "notistack";
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import Page from "src/shared/Page";
import { getUniversity } from "src/utils/mng_user";
import DragnDropZone from "../../../shared/DragnDropZone";
import { requirePrivateKeyHex } from "../../../utils/keyholder";
import { ERR_TOP_CENTER, SUCCESS_TOP_CENTER } from "../../../utils/snackbar-utils";
import { startUploadFile, uploadFileFail, uploadFileSuccess } from "./redux";
import TeacherDataExample from "./TeacherDataExample";
import TeacherUploadHistory from "./TeacherUploadHistory";

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

export default function CreateTeacherAccount() {
    const cls = useStyles();
    const uploading = useSelector((state) => state.teacherSlice.uploading);
    const dp = useDispatch();
    const { enqueueSnackbar } = useSnackbar();
    const university = getUniversity();

    async function hdUploadFile(files) {
        dp(startUploadFile());
        const formData = new FormData();
        formData.append("excel-file", files[0]);
        formData.append("university", university);
        try {
            const response = await axios.post("/create-professor/", formData);
            enqueueSnackbar("Tạo tài khoản các giảng viên thành công!", SUCCESS_TOP_CENTER);
            dp(uploadFileSuccess());
        } catch (error) {
            dp(uploadFileFail());
            console.error(error);
            if (error.response) enqueueSnackbar(JSON.stringify(error.response.data), ERR_TOP_CENTER);
        }
    }

    return (
        <Page title="Tạo tài khoản giảng viên ">
            <div className={cls.root}>
                <TeacherDataExample></TeacherDataExample>
                <DragnDropZone onDropAccepted={hdUploadFile} uploading={uploading}></DragnDropZone>
                <TeacherUploadHistory></TeacherUploadHistory>
            </div>
        </Page>
    );
}
