import { Box, Divider, makeStyles, Paper, Typography } from "@material-ui/core";
import React from "react";
import { useSelector } from "react-redux";

const useStyles = makeStyles((theme) => ({
  root: {
    padding: theme.spacing(2),
  },
}));

export default function EncryptedSubjectTable(props) {
  const cls = useStyles();
  const subjects = useSelector((state) => state.shareCertificateSlice.selectedEduProgram.subjects);
  return (
    <div>
      <Paper className={cls.root}>
        <Box mb={1}>
          <Typography variant="h4">Thông tin bảng điểm (dạng mã hóa)</Typography>
        </Box>
        <Divider></Divider>
        <Box mt={2}>
          {subjects.map((subject, index) => (
            <React.Fragment key={index}>
              {subject.versions.map((version, index) => (
                <Box key={index} mt={2} style={{ wordWrap: "break-word" }}>
                  {version.cipher}
                </Box>
              ))}
            </React.Fragment>
          ))}
        </Box>
      </Paper>
    </div>
  );
}
