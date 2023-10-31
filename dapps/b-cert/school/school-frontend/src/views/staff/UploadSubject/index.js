import { makeStyles } from "@material-ui/core";
import { useSnackbar } from "notistack";
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import DragnDropZone from "../../../shared/DragnDropZone";
import Page from "src/shared/Page";
import { getToken } from "src/utils/mng-token";
import SubjectDataExample from "./SubjectDataExample";
import { startUploadFile, uploadFileFail, uploadFileSuccess } from "./redux";
import UploadedSubjectTable from "./UploadedSubjectTable";
import { ERR_TOP_CENTER, SUCCESS_BOTTOM_CENTER, SUCCESS_TOP_CENTER } from "../../../utils/snackbar-utils";
import axios from "axios";
import { getUniversity } from "src/utils/mng_user";

const useStyles = makeStyles((theme) => ({
    root: {
        "& > *": {
            marginBottom: theme.spacing(2),
            "&:last-child": {
                marginBottom: 0,
            },
        },
        paddingBottom: theme.spacing(2.5),
        // height: "calc(150% + 50px)",
    },
}));

export default function UploadSubject() {
    const cls = useStyles();
    const uploading = useSelector((state) => state.teacherSlice.uploading);
    const universityProfile = useSelector((state) => state.profileSlice);
    const dp = useDispatch();
    const { enqueueSnackbar } = useSnackbar();
    const university = getUniversity();

    async function hdUploadFile(files) {
        dp(startUploadFile());
        const formData = new FormData();
        formData.append("excel-file", files[0]);
        formData.append("university", universityProfile.id || "");
        try {
            const response = await axios.post("/create-subject/", formData);
            enqueueSnackbar("Tạo các môn học thành công!", SUCCESS_TOP_CENTER);
            dp(uploadFileSuccess());
        } catch (error) {
            dp(uploadFileFail());
            console.error(error);
            if (error.response) enqueueSnackbar(JSON.stringify(error.response.data), ERR_TOP_CENTER);
        }
    }

    return (
        <Page title="Upload môn học">
            <div className={cls.root}>
                <SubjectDataExample></SubjectDataExample>
                <DragnDropZone onDropAccepted={hdUploadFile} uploading={uploading}></DragnDropZone>
                <UploadedSubjectTable></UploadedSubjectTable>
            </div>
        </Page>
    );
}
