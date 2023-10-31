import { Box, Divider, makeStyles, Paper, Typography } from "@material-ui/core";
import { useSelector } from "react-redux";

const useStyles = makeStyles((theme) => ({
  root: {
    padding: theme.spacing(2),
  },
}));

export default function EncryptedCertInfo(props) {
  const cls = useStyles();
  const cipher = useSelector((state) => {
    const versions = state.shareCertificateSlice.selectedEduProgram.certificate?.versions;
    if (!versions) {
      return <Typography>Chưa có bằng cấp!</Typography>;
    }
    // backend already sort the arrays
    return versions[versions.length - 1].cipher;
  });
  return (
    <div>
      <Paper className={cls.root}>
        <Box mb={1}>
          <Typography variant="h4">Thông tin bằng cấp (dạng mã hóa)</Typography>
        </Box>
        <Divider></Divider>
        <Box mt={2} style={{ wordWrap: "break-word" }}>
          {cipher}
        </Box>
      </Paper>
    </div>
  );
}
