import { makeStyles } from "@material-ui/core";
import { useSnackbar } from "notistack";
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import Page from "src/shared/Page";
import { getToken } from "src/utils/mng-token";
import DragnDropZone from "../../../shared/DragnDropZone";
import { requirePrivateKeyHex } from "../../../utils/keyholder";
import { ERR_TOP_CENTER, SUCCESS_BOTTOM_CENTER } from "../../../utils/snackbar-utils";
import BureauDataExample from "./BureauDataExample";
import BureauUploadHistory from "./BureauUploadHistory";
import { startUploadFile, uploadFileFail, uploadFileSuccess } from "./redux";

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

export default function CreateBureauAccount() {
  const cls = useStyles();
  const uploading = useSelector((state) => state.bureauSlice.uploading);
  const dp = useDispatch();
  const { enqueueSnackbar } = useSnackbar();

  async function hdUploadFile(files) {
    const privateKeyHex = await requirePrivateKeyHex(enqueueSnackbar);
    dp(startUploadFile());
    const formData = new FormData();
    formData.append("excel-file", files[0]);
    formData.append("privateKeyHex", privateKeyHex);
    const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/v1.2/staff/create-bureau`, {
      method: "POST",
      headers: { Authorization: getToken() },
      body: formData,
    });
    if (!response.ok) {
      dp(uploadFileFail());
      enqueueSnackbar(`${response.status}: ${await response.text()}`, ERR_TOP_CENTER);
    } else {
      const result = await response.json();
      dp(uploadFileSuccess(result));
      enqueueSnackbar("Tạo tài khoản cho các giáo vụ thành công!", SUCCESS_BOTTOM_CENTER);
    }
  }

  return (
    <Page title="Tạo tài khoản giáo vụ ">
      <div className={cls.root}>
        <BureauDataExample></BureauDataExample>
        <DragnDropZone onDropAccepted={hdUploadFile} uploading={uploading}></DragnDropZone>
        <BureauUploadHistory></BureauUploadHistory>
      </div>
    </Page>
  );
}
