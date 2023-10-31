import { makeStyles } from "@material-ui/core";
import axios from "axios";
import { useSnackbar } from "notistack";
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import Page from "src/shared/Page";
import DragnDropZone from "../../../shared/DragnDropZone";
import { requirePrivateKeyHex } from "../../../utils/keyholder";
import { ERR_TOP_CENTER, SUCCESS_TOP_CENTER } from "../../../utils/snackbar-utils";
import CertificateDataExample from "./CertificateDataExample";
import { startUploadFile, uploadFileFail, uploadFileSuccess } from "./redux";
import UploadedCertificateTable from "./UploadedCertificateTable";
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
    },
}));

export default function UploadCertificate() {
    const cls = useStyles();
    const uploading = useSelector((state) => state.certificateSlice.uploading);
    const dp = useDispatch();
    const { enqueueSnackbar } = useSnackbar();
    const universityProfile = useSelector((state) => state.profileSlice);
    const university_id = getUniversity();

    async function hdUploadFile(files) {
        // const privateKeyHex = await requirePrivateKeyHex(enqueueSnackbar);
        dp(startUploadFile());
        const formData = new FormData();
        formData.append("university_id", universityProfile.id || "");
        formData.append("excel_file", files[0]);
        // formData.append("privateKeyHex", privateKeyHex);
        try {
            const response = await axios.post("/create-certificate", formData);
            enqueueSnackbar("Upload file thành công!", SUCCESS_TOP_CENTER);
            dp(uploadFileSuccess(response.data));
        } catch (error) {
            console.error(error);
            if (error.response) enqueueSnackbar(JSON.stringify(error.response.data), ERR_TOP_CENTER);
            dp(uploadFileFail());
        }
    }

    return (
        <Page title="Upload bằng cấp">
            <div className={cls.root}>
                <CertificateDataExample></CertificateDataExample>
                <DragnDropZone onDropAccepted={hdUploadFile} uploading={uploading}></DragnDropZone>
                <UploadedCertificateTable></UploadedCertificateTable>
            </div>
        </Page>
    );
}
