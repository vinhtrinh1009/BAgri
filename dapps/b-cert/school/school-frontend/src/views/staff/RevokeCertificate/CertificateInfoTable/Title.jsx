import {
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  makeStyles,
  Typography,
} from "@material-ui/core";
import CheckIcon from "@material-ui/icons/Check";
import ErrorOutlineIcon from "@material-ui/icons/ErrorOutline";
import axios from "axios";
import { useSnackbar } from "notistack";
import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { getUniversity } from "src/utils/mng_user";
import { requirePrivateKeyHex } from "../../../../utils/keyholder";
import { ERR_TOP_CENTER, INFO_TOP_CENTER, SUCCESS_TOP_CENTER } from "../../../../utils/snackbar-utils";
import { setDocument } from "../redux";

const useStyles = makeStyles((theme) => ({
  root: {},
  typo: {
    display: "flex",
    alignItems: "center",
  },
}));

export default function Title({ cert }) {
  const cls = useStyles();
  const dp = useDispatch();
  const { enqueueSnackbar } = useSnackbar();
  const [confirmDialog, setConfirmDialog] = useState(null);
  const university = getUniversity()

  async function hdRevoke(cert) {
    const dialog = (
      <Dialog open={true} onClose={() => setConfirmDialog(null)}>
        <DialogTitle>
          <Typography variant="h4">{"Thu hồi bằng cấp?"}</Typography>
        </DialogTitle>
        <DialogContent>
          <DialogContentText>Sau khi thu hồi, bằng cấp sẽ không còn hợp lệ và không thể chia sẻ với người khác!</DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setConfirmDialog(null)}>Cancel</Button>
          <Button
            color="primary"
            onClick={() => {
              setConfirmDialog(null);
              revoke();
            }}
          >
            Yes
          </Button>
        </DialogActions>
      </Dialog>
    );

    async function revoke() {
    //   const privateKeyHex = await requirePrivateKeyHex(enqueueSnackbar);
      try {
        const response = await axios.patch("/update-certificate/"+cert.student_id+"/", {"university": university, "action": "revoke"});
        enqueueSnackbar("Thu hồi bằng cấp thành công!", INFO_TOP_CENTER);
        dp(setDocument(response.data));
      } catch (error) {
        console.error(error);
        if (error.response) enqueueSnackbar(JSON.stringify(error.response.data), ERR_TOP_CENTER);
      }
    }

    setConfirmDialog(dialog);
  }

  async function hdReactive(cert) {
    // const privateKeyHex = await requirePrivateKeyHex(enqueueSnackbar);
    try {
      const response = await axios.patch("/update-certificate/"+cert.student_id+"/", {"university": university, "action": "reactive"});
      enqueueSnackbar("Cấp lại bằng cấp thành công!", SUCCESS_TOP_CENTER);
      dp(setDocument(response.data));
    } catch (error) {
      console.error(error);
      if (error.response) enqueueSnackbar(JSON.stringify(error.response.data), ERR_TOP_CENTER);
    }
  }

  return (
    <Box px={2} py={1} display="flex" justifyContent="space-between" alignItems="center">
      {cert.status === false ? (
        <>
          <Typography variant="h4" className={cls.typo}>
            Trạng thái bằng cấp: &nbsp; <ErrorOutlineIcon color="secondary"></ErrorOutlineIcon>
          </Typography>
          {/* <Typography variant="h4" className={cls.typo}>
            {`Version: ${cert.version}`}
          </Typography>
          <Typography variant="h4" className={cls.typo}>
            {`Timestamp: ${cert.timestamp}`}
          </Typography> */}
          <Button color="primary" variant="outlined" onClick={(e) => hdReactive(cert)}>
            Cấp lại
          </Button>
        </>
      ) : (
        <>
          <Typography variant="h4" className={cls.typo}>
            Trạng thái bằng cấp: &nbsp; <CheckIcon style={{ color: "green" }}></CheckIcon>
          </Typography>
          {/* <Typography variant="h4" className={cls.typo}>
            {`Version: ${cert.version}`}
          </Typography>
          <Typography variant="h4" className={cls.typo}>
            {`Timestamp: ${cert.timestamp}`}
          </Typography> */}
          <Button color="secondary" variant="outlined" onClick={(e) => hdRevoke(cert)}>
            Thu hồi
          </Button>
          {confirmDialog}
        </>
      )}
    </Box>
  );
}
