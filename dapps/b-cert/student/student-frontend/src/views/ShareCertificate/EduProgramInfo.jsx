import { Box, makeStyles, Paper, TextField, Typography } from "@material-ui/core";
import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getUniversity, getUser } from "src/utils/mng_user";
import { setEduProgram } from "./redux";
import { useSnackbar } from "notistack"
import axios from "axios"
import { ERR_TOP_CENTER, SUCCESS_BOTTOM_CENTER } from "src/utils/snackbar-utils"


const useStyles = makeStyles((theme) => ({
    root: {
      "& .MuiFormLabel-root.Mui-disabled": {
        color: theme.palette.primary.main,
      },
      "& .MuiInputBase-input.Mui-disabled": {
        color: "black",
      },
    },
    head: {
      width: "95%",
      margin: "auto",
      padding: theme.spacing(2.5, 2),
      backgroundColor: theme.palette.primary.main,
      color: "white",
      position: "relative", // this bring head foreground
    },
    body: { width: "100%", marginTop: "-32px" },
    box: {
      padding: theme.spacing(8, 3, 3, 3),
      "& > *": {
        marginBottom: theme.spacing(4),
        "&:last-child": {
          marginBottom: 0,
        },
      },
    },
  }));

export default function EduProgramInfo() {
  const cls = useStyles()
  const eduProgram = useSelector((state) => state.shareCertificateSlice.eduProgram);
//   const university = getUniversity()
//   const user = getUser()
//   const dp = useDispatch();
//   const { enqueueSnackbar } = useSnackbar();

//   useEffect(() => {
//     fetchEduProgram();
//     // eslint-disable-next-line react-hooks/exhaustive-deps
//   }, []);


//   function fetchEduProgram(){
//       axios.get('/student/'+user+'/').then(res =>{
//           dp(setEduProgram(res.data))
//       }).catch(error => {
//           enqueueSnackbar(JSON.stringify(error.response.data), ERR_TOP_CENTER)
//       })
//   }

  return (
    <Box className={cls.root}>
      <Paper className={cls.head}>
        <Typography variant="h3">Thông tin học tập</Typography>
      </Paper>
      <Box className={cls.body}>
        <Paper>
          <Box className={cls.box}>
            <TextField
                InputLabelProps={{ shrink: true }}
                fullWidth
                label="Tên Trường"
                value={eduProgram?.university.university_name}
                onChange={(e) => {console.log(e.target.value)}}
                disabled={true}
            ></TextField>
            <TextField
              InputLabelProps={{ shrink: true }}
              fullWidth
              label="Hình thức đào tạo"
              rows={4}
              value={eduProgram?.edu_program}
              onChange={(e) => {console.log(e.target.value)}}
              disabled={true}
            ></TextField>
          </Box>
        </Paper>
      </Box>
    </Box>
  );
}
