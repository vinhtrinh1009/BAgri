import { Box, Button, Grid, makeStyles, Paper, TextField, Typography } from "@material-ui/core";
import { useSnackbar } from "notistack";
import { useState } from "react";
import { useDispatch } from "react-redux";
import { getToken } from "../../utils/mng-token";
import { addSawtoothAccount } from "./redux";

const useStyles = makeStyles((theme) => ({
  root: {},
  head: { padding: theme.spacing(2), backgroundColor: theme.palette.primary.main, color: "white" },
  subtitle: {
    marginBottom: theme.spacing(3),
    // fontWeight: 400,
  },
}));

export default function AddAccount(props) {
  const cls = useStyles();
  const [formState, setFormState] = useState({
    publicKeyHex: "",
    privateKeyHex: "",
    note: "",
  });

  const { enqueueSnackbar } = useSnackbar();
  const dp = useDispatch();

  async function hdAddAccount(e) {
    try {
      e.preventDefault();
      if (formState.publicKeyHex === "") {
        enqueueSnackbar("Public key is require!", { variant: "error", anchorOrigin: { vertical: "top", horizontal: "center" } });
        return;
      }
      // TODO: validate publicKeyHex, privateKeyHex(if exists)

      let response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/student/sawtooth-accounts`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: getToken() },
        body: JSON.stringify(formState),
      });

      if (!response.ok) {
        const error = await response.json();
        enqueueSnackbar("Something went wrong: " + JSON.stringify(error), {
          variant: "error",
          anchorOrigin: { vertical: "top", horizontal: "center" },
        });
      } else {
        dp(addSawtoothAccount(formState));
        setFormState({
          publicKeyHex: "",
          privateKeyHex: "",
          note: "",
        });
        enqueueSnackbar("Thêm tài khoản thành công!", { variant: "success", anchorOrigin: { vertical: "bottom", horizontal: "center" } });
      }
    } catch (error) {
      alert(error);
    }
  }
  return (
    <Paper>
      <Typography variant="h3" className={cls.head}>
        Thêm tài khoản
      </Typography>

      <Box px={2} py={3}>
        <Typography variant="h5" className={cls.subtitle}>
          Thêm tài khoản bằng public/private key
        </Typography>
        <Grid container spacing={4} alignItems="flex-end">
          <Grid item xs={12} md={4}>
            <TextField
              label="Public key"
              InputLabelProps={{ shrink: true }}
              fullWidth
              value={formState.publicKeyHex}
              onChange={(e) => setFormState({ ...formState, publicKeyHex: e.target.value })}
            ></TextField>
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField
              label="Private key (optional)"
              InputLabelProps={{ shrink: true }}
              InputProps={{ type: "password" }}
              fullWidth
              value={formState.privateKeyHex}
              onChange={(e) => setFormState({ ...formState, privateKeyHex: e.target.value })}
            ></TextField>
          </Grid>
          <Grid item xs={12} md={2}>
            <TextField
              label="Ghi chú"
              InputLabelProps={{ shrink: true }}
              fullWidth
              value={formState.note}
              onChange={(e) => setFormState({ ...formState, note: e.target.value })}
            ></TextField>
          </Grid>
          <Grid item xs={12} md={2}>
            <Box textAlign="right">
              <Button variant="contained" color="primary" onClick={hdAddAccount}>
                Thêm tài khoản
              </Button>
            </Box>
          </Grid>
        </Grid>
      </Box>

      {/* <Box my={2} p={2} display="flex" justifyContent="space-between">
        <Typography variant="h5">Hoặc sử dụng ví B4E Wallet để chọn tài khoản muốn thêm</Typography>
        <Button variant="contained" color="primary">
          Sử dụng ví
        </Button>
      </Box> */}
    </Paper>
  );
}
