import React, { useEffect, useState } from "react";
import { Box, Button, Paper, TextField } from "@material-ui/core";
import axios from "axios";
import { useDispatch } from "react-redux";
import { setDocument } from "./redux";
import { useSnackbar } from "notistack";
import { ERR_TOP_CENTER, INFO_TOP_CENTER } from "../../../utils/snackbar-utils";

export default function SearchBox(props) {
  const [studentId, setStudentId] = useState("");
  const dp = useDispatch();
  const { enqueueSnackbar } = useSnackbar();

  // remove redux cached on unmount
  useEffect(() => {
    return () => {
      dp(setDocument(null));
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function hdSubmitStudentId() {
    try {
      const response = await axios.get(`/search-certificate/?student=${studentId}`);
      if (!response.data) enqueueSnackbar("Không tìm thấy bằng cấp của " + studentId, INFO_TOP_CENTER);
      dp(setDocument(response.data));
    } catch (error) {
      console.error(error);
      if (error.response) enqueueSnackbar(JSON.stringify(error.response.data), ERR_TOP_CENTER);
    }
  }
  return (
    <Paper>
      <Box px={2} py={2} display="flex" alignItems="flex-end">
        <TextField
          label="Mã số sinh viên"
          InputLabelProps={{ shrink: true }}
          autoFocus
          value={studentId}
          onChange={(e) => setStudentId(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              hdSubmitStudentId();
            }
          }}
        ></TextField>
        <Box px={2}>
          <Button variant="contained" color="primary" onClick={hdSubmitStudentId}>
            Go
          </Button>
        </Box>
      </Box>
    </Paper>
  );
}
