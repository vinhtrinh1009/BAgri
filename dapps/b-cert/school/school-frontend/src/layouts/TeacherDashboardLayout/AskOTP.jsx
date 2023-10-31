import { Box, Button, Dialog, DialogContent, DialogTitle, Grid, TextField, Typography } from "@material-ui/core";
import axios from "axios";
import React, { createRef, useState } from "react";

export default function AskOTP({ open, hdCancel, hdError, hdSuccess, hdFail, classes }) {
  const [OTP, setOTP] = useState(["", "", "", "", "", ""]);
  const [refs, setRefs] = useState([...Array(6).keys()].map(() => createRef()));

  function hdKeyUp(e, index) {
    const clonedOTP = [...OTP];
    if (e.keyCode === 8) {
      clonedOTP[index] = "";
      if (index > 0) {
        refs[index - 1].current.focus();
      }
    } else {
      clonedOTP[index] = e.key;
      if (index < 5) {
        refs[index + 1].current.focus();
      }
    }
    setOTP(clonedOTP);
  }

  async function sendOTP() {
    const otpString = OTP.join("");
    try {
      const response = await axios.post("/acc/2fa/verify", { OTP: otpString });
      if (!response.data.ok) {
        hdFail();
      } else {
        hdSuccess();
      }
    } catch (error) {
      hdError(error);
    }
  }

  return (
    <Dialog
      open={open}
      maxWidth="sm"
      fullWidth
      onClose={() => {
        hdCancel();
      }}
    >
      <DialogTitle>Xác thực 2 bước</DialogTitle>
      <DialogContent>
        <Typography align="center" variant="h4">
          Nhập mã OTP:
        </Typography>
        <Box mb={2}></Box>
        <Grid container spacing={2} justify="center">
          {[...Array(6).keys()].map((item, index) => (
            <Grid item key={index}>
              <TextField
                inputProps={{ size: 1 }}
                variant="outlined"
                color="primary"
                value={OTP[index]}
                onKeyUp={(e) => hdKeyUp(e, index)}
                inputRef={refs[index]}
                autoFocus={index === 0}
              ></TextField>
            </Grid>
          ))}
        </Grid>
        <Box mt={2} textAlign="right">
          <Button onClick={hdCancel} style={{ marginRight: "16px" }}>
            Canel
          </Button>
          <Button variant="contained" color="primary" onClick={sendOTP}>
            Send
          </Button>
        </Box>
      </DialogContent>
    </Dialog>
  );
}
