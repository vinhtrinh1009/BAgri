import { Box, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from "@material-ui/core";
import axios from "axios";
import { useSnackbar } from "notistack";
import { useState } from "react";
import Page from "../../../shared/Page";
import { ERR_TOP_CENTER } from "../../../utils/snackbar-utils";
import InputClassId from "./InputClassId";
import RowWithCollapseContent from "./RowWithCollapseContent.jsx";

export default function EditGrade() {
  const [claxx, setClaxx] = useState([]);
  const [classId, setClassId] = useState("");
  const { enqueueSnackbar } = useSnackbar();
  const teacher_id = localStorage.getItem("user");

  async function hdGetClass() {
    try {
      const response = await axios.get("results/?class=" + classId + "&teacher=" + teacher_id);
      console.log(response.data)
      setClaxx(response.data);
    } catch (error) {
      console.error(error);
      if (error.response) enqueueSnackbar(JSON.stringify(error.response.data), ERR_TOP_CENTER);
    }

  }

  return (
    <Page title="Sửa điểm">
      <InputClassId {...{ classId, setClassId, hdGetClass }}></InputClassId>
      <Box mt={2}> </Box>

      {/* if not found */}
      {claxx === null && (
        <Paper>
          <Box p={2}>
            <Typography>{`Không tìm thấy lớp ${classId}`}</Typography>
          </Box>
        </Paper>
      )}

      {/* if found but not submit yet */}
      {claxx && claxx.status && (
        <Paper>
          <Box p={2}>
            <Typography>{`Lớp ${classId} chưa được nhập điểm!`}</Typography>
          </Box>
        </Paper>
      )}

      {/* if found and already submited */}
      {claxx && !claxx.status && (
        <Paper>
          <Box px={1} py={2}>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>STT</TableCell>
                    <TableCell>MSSV</TableCell>
                    <TableCell>Họ và tên</TableCell>
                    <TableCell>Ngày sinh</TableCell>
                    <TableCell>Email</TableCell>
                    <TableCell></TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {claxx.map((resultRecord, index) => {
                    return (
                      <RowWithCollapseContent
                        key={index}
                        record={resultRecord}
                        index={index}
                        claxx={claxx}
                        setClaxx={setClaxx}
                        getAllResult={hdGetClass}
                      ></RowWithCollapseContent>
                    );
                  })}
                </TableBody>
              </Table>
            </TableContainer>
          </Box>
        </Paper>
      )}
    </Page>
  );
}
