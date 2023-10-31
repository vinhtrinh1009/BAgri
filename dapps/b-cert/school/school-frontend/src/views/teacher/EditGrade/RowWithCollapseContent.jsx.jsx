import { Box, Collapse, IconButton, makeStyles, TableCell, TableRow } from "@material-ui/core";
import KeyboardArrowDownIcon from "@material-ui/icons/KeyboardArrowDown";
import KeyboardArrowUpIcon from "@material-ui/icons/KeyboardArrowUp";
import axios from "axios";
import { useSnackbar } from "notistack";
import { useState } from "react";
import AskOTP from "../../../layouts/TeacherDashboardLayout/AskOTP";
import { requirePrivateKeyHex } from "../../../utils/keyholder";
import { isEnable2FA } from "../../../utils/mng-2fa";
import { ERR_TOP_CENTER, INFO_TOP_CENTER, SUCCESS_TOP_CENTER } from "../../../utils/snackbar-utils";
import EditGradeForm from "./EditGradeForm";
import EditGradeHistory from "./EditGradeHistory";

const useRowStyles = makeStyles({
  root: {
    "& > *": {
      borderBottom: "unset",
    },
  },
  timeline: {
    paddingLeft: 0,
    "& .MuiTimelineItem-missingOppositeContent:before": {
      flex: 0,
      padding: 0,
    },
  },
});

export default function RowWithCollapseContent(props) {
  const { claxx, record, index, setClaxx, getAllResult } = props;
  const [open, setOpen] = useState(false);
  const cls = useRowStyles();
  const { enqueueSnackbar } = useSnackbar();

  const [askOTPDialog, setAskOTPDialog] = useState(null);
  console.log(record)
  async function hdSubmit(resultID, halfSemesterPoint, finalSemesterPoint) {
    // if (isEnable2FA()) {
    //   setAskOTPDialog(
    //     <AskOTP
    //       open={true}
    //       hdCancel={() => setAskOTPDialog(null)}
    //       hdFail={() => {
    //         enqueueSnackbar("Mã OTP không chính xác, vui lòng thử lại", ERR_TOP_CENTER);
    //       }}
    //       hdSuccess={() => {
    //         setAskOTPDialog(null);
    //         sendEditedGrade(resultID, halfSemesterPoint, finalSemesterPoint);
    //       }}
    //     ></AskOTP>
    //   );
    // } else {
    sendEditedGrade(resultID, halfSemesterPoint, finalSemesterPoint);
    // }
  }

  async function sendEditedGrade(resultID, halfSemesterPoint, finalSemesterPoint) {
    // const privateKeyHex = await requirePrivateKeyHex(enqueueSnackbar);
    if(parseFloat(halfSemesterPoint)<0 || parseFloat(halfSemesterPoint)>10 || !parseFloat(halfSemesterPoint)) {
        return enqueueSnackbar("Result must be float and between 0 to 10", INFO_TOP_CENTER)
    }
    if(parseFloat(finalSemesterPoint)<0 || parseFloat(finalSemesterPoint)>10 || !parseFloat(finalSemesterPoint)) {
        return enqueueSnackbar("Result must be float and between 0 to 10", INFO_TOP_CENTER)
    } 
    try {
      const response = await axios.patch("results/" + resultID + "/", {
        "middle_score": parseFloat(halfSemesterPoint),
        "final_score": parseFloat(finalSemesterPoint)
      });
      // let clonedClass = claxx;
      // clonedClass[index] = response.data;
      // console.log(clonedClass)
      // setClaxx(clonedClass);
      getAllResult();
      enqueueSnackbar("Sửa điểm thành công!", SUCCESS_TOP_CENTER);
    } catch (error) {
      console.error(error);
      if (error.response) enqueueSnackbar(JSON.stringify(error.response.data), ERR_TOP_CENTER);
    }
  }

  return (
    <>
      <TableRow className={cls.root}>
        <TableCell>{index + 1}</TableCell>
        <TableCell>{record.student.student_id}</TableCell>
        <TableCell>{record.student.user.full_name}</TableCell>
        <TableCell>{record.student.user.birthday}</TableCell>
        <TableCell>{record.student.user.email}</TableCell>
        <TableCell>
          <IconButton size="small" onClick={() => setOpen(!open)}>
            {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
          </IconButton>
        </TableCell>
      </TableRow>
      <TableRow>
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
          <Collapse in={open} timeout="auto" unmountOnExit>
            <Box px={1} pb={3}>
              <Box p={2} border="1px solid grey">
                {/* <EditGradeHistory student={student}></EditGradeHistory> */}
                <Box mt={4}></Box>
                <EditGradeForm hdSubmit={hdSubmit} index={index} recordId={record.id} oldMidtermScore={record.middle_score} oldFinalScore={record.final_score}></EditGradeForm>
                {askOTPDialog}
              </Box>
            </Box>
          </Collapse>
        </TableCell>
      </TableRow>
    </>
  );
}
