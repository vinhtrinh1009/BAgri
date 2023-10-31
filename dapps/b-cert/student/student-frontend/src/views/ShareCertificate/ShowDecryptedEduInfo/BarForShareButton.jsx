import { Box, Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, makeStyles, Paper } from "@material-ui/core";
import { Alert, AlertTitle } from "@material-ui/lab";
import { useSnackbar } from "notistack";
import { useState } from "react";
import { useSelector } from "react-redux";
import { getToken } from "../../../utils/mng-token";
import FileSaver from "file-saver";
import { ERR_TOP_CENTER } from "../../../utils/snackbar-utils";
import axios from "axios";

const useStyles = makeStyles((theme) => ({
  root: {
    padding: theme.spacing(2),
    "& .MuiTypography-gutterBottom": {
      marginBottom: 0,
    },
  },
}));

export default function BarForShareButton(props) {
  const cls = useStyles();
  const decryptedData = useSelector((state) => state.shareCertificateSlice.decryptedEduProgram);
  const selectedAccount = useSelector((state) => state.shareCertificateSlice.selectedAccount);

  const [token, setToken] = useState(null);
  const { enqueueSnackbar } = useSnackbar();

  async function hdClick() {
    if (!decryptedData.certificate) {
      enqueueSnackbar("Chưa có bằng cấp để chia sẻ!", ERR_TOP_CENTER);
      return;
    }
    // supose backend already sort versions
    if (decryptedData.certificate.versions[0].type === "revoke") {
      enqueueSnackbar("Không thể chia sẻ bằng cấp đã bị thu hồi!", ERR_TOP_CENTER);
      return;
    }

    try {
      const response = await axios.post("/student/gen-token", { publicKeyHex: selectedAccount.publicKeyHex, ...decryptedData });
      setToken(response.data.token);
    } catch (error) {
      enqueueSnackbar(JSON.stringify(error.response.data), ERR_TOP_CENTER);
    }
  }

  return (
    <Paper className={cls.root}>
      <Box display="flex" alignItems="center">
        <Box flexGrow={1}>
          <Alert severity="success">
            <AlertTitle>Giải mã dữ liệu thành công!</AlertTitle>
          </Alert>
        </Box>
        {/* {decryptedData.certificate && (
          <Box pl={2} flexShrink={0}>
            <Button variant="contained" color="primary" onClick={hdClick}>
              Chia sẻ
            </Button>
          </Box>
        )} */}
        {
          <Box pl={2} flexShrink={0}>
            <Button variant="contained" color="primary" onClick={hdClick} disabled={Boolean(!decryptedData.certificate)}>
              Chia sẻ
            </Button>
          </Box>
        }
      </Box>
      <TokenDialog token={token} setToken={setToken}></TokenDialog>
    </Paper>
  );
}

function TokenDialog({ token, setToken }) {
  return (
    <Dialog open={Boolean(token)} onClose={(e) => setToken(null)}>
      <DialogTitle>Token</DialogTitle>
      <DialogContent>
        <DialogContentText style={{ wordWrap: "break-word" }}>{token} </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button
          color="primary"
          onClick={(e) => {
            navigator.clipboard.writeText(token);
            setToken(null);
          }}
        >
          Copy
        </Button>
        <Button
          color="primary"
          onClick={(e) => {
            var blob = new Blob([token], { type: "text/plain;charset=utf-8" });
            FileSaver.saveAs(blob, "B4E-Certificate-Token.jwt");
            setToken(null);
          }}
        >
          Download
        </Button>
      </DialogActions>
    </Dialog>
  );
}
