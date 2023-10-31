import { Box, Button, makeStyles, Paper } from "@material-ui/core";
import { Alert, AlertTitle } from "@material-ui/lab";
import axios from "axios";
import { useSnackbar } from "notistack";
import { useDispatch, useSelector } from "react-redux";
import { requirePrivateKeyHex } from "../../../utils/keyholder";
import { ERR_TOP_CENTER } from "../../../utils/snackbar-utils";
import { setDecryptedEduProgram } from "../redux";

const useStyles = makeStyles((theme) => ({
  root: {
    padding: theme.spacing(2),
    "& .MuiTypography-gutterBottom": {
      marginBottom: 0,
    },
  },
}));

export default function BarForDecryptedButton() {
  const selectedAccount = useSelector((state) => state.shareCertificateSlice.selectedAccount);
  const selectedEduProgram = useSelector((state) => state.shareCertificateSlice.selectedEduProgram);

  const cls = useStyles();
  const dp = useDispatch();
  const { enqueueSnackbar } = useSnackbar();

  async function hdClick() {
    let privateKeyHex = selectedAccount.privateKey;
    if (!privateKeyHex) {
      privateKeyHex = await requirePrivateKeyHex(enqueueSnackbar);
    }
    try {
      const response = await axios.post("/student/decrypt-eduprogram", { privateKeyHex, selectedEduProgram });
      dp(setDecryptedEduProgram(response.data));
    } catch (error) {
      console.error(error);
      error.response && enqueueSnackbar(JSON.stringify(error.response.data), ERR_TOP_CENTER);
    }
  }

  return (
    <Paper className={cls.root}>
      <Box display="flex" alignItems="center">
        <Box flexGrow={1}>
          <Alert severity="success">
            <AlertTitle>Lấy dữ liệu bản mã thành công!</AlertTitle>
          </Alert>
        </Box>
        <Box pl={2} flexShrink={0}>
          <Button variant="contained" color="primary" onClick={hdClick}>
            Giải mã
          </Button>
        </Box>
      </Box>
    </Paper>
  );
}
