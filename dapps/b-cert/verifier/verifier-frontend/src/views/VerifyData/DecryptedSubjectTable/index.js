import {
  Box,
  Divider,
  makeStyles,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@material-ui/core";
import React from "react";
import { useSelector } from "react-redux";
import DecryptedSubject from "./DecryptedSubject";

const useStyles = makeStyles((theme) => ({
  root: {
    padding: theme.spacing(0, 2, 2, 2),
  },
  typo: {
    flexGrow: 1,
  },
}));

export default function DecryptedSubjectInfo(props) {
  const cls = useStyles();
  const subjects = useSelector((state) => state.appSlice.decodedToken.subjects);

  return (
    <div>
      <Paper className={cls.root}>
        <Box pt={2} pb={1} display="flex" alignItems="center">
          <Typography variant="h4" className={cls.typo}>
            Thông tin bảng điểm
          </Typography>
          {/* <CircularProgress size="1.5rem"></CircularProgress> */}
        </Box>
        <Divider></Divider>
        <TableContainer>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Kì học</TableCell>
                <TableCell>Mã HP</TableCell>
                <TableCell>Tên HP</TableCell>
                <TableCell>Số TC</TableCell>
                <TableCell>Điểm GK</TableCell>
                <TableCell>Điểm CK</TableCell>
                <TableCell>Mã GV</TableCell>
                <TableCell>Tên GV</TableCell>
                <TableCell>Txid</TableCell>
                <TableCell>Tính toàn vẹn</TableCell>
                {/* <TableCell>Timestamp</TableCell> */}
              </TableRow>
            </TableHead>
            <TableBody>
              {subjects.map((subject, subjectIndex) => (
                <DecryptedSubject subject={subject} subjectIndex={subjectIndex} key={subjectIndex}></DecryptedSubject>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </div>
  );
}
