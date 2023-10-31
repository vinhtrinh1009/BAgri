import { Box, Divider, Grid, makeStyles, Paper, Table, TableBody, TableCell, TableContainer, TableRow, Tooltip, Typography } from "@material-ui/core";
import CheckIcon from "@material-ui/icons/Check";
import ErrorOutlineIcon from "@material-ui/icons/ErrorOutline";
import { useSelector } from "react-redux";
import { getLinkFromTxid } from "../../../utils/utils";

const useStyles = makeStyles((theme) => ({
    root: {
        padding: theme.spacing(0, 2, 2, 2),
    },
}));

export default function DecryptedCertInfo(props) {
    const cls = useStyles();
    const versions = useSelector((state) => state.shareCertificateSlice.decryptedEduProgram?.certificate?.versions);
    const certificateData = useSelector((state) => state.shareCertificateSlice?.certificateData);

    return (
        <div>
            <Paper className={cls.root} style={{ marginTop: "15px" }}>
                {!certificateData && (
                    <>
                        <Box pt={2} pb={1}>
                            <Typography variant="h4" gutterBottom>
                                Thông tin bằng cấp
                            </Typography>
                            <Divider></Divider>
                            <Typography style={{ paddingTop: "8px" }}>Chưa có bằng cấp!</Typography>
                        </Box>
                    </>
                )}
                {certificateData && <CertTable cert={certificateData}></CertTable>}
            </Paper>
        </div>
    );
}

function CertTable({ cert }) {
    console.log(cert);
    const [certPart1, certPart2] = separateCertificate(cert);
    return (
        <>
            <Box pt={2} pb={1} display="flex" justifyContent="space-between" alignItems="center">
                <Typography variant="h4">Thông tin bằng cấp</Typography>
                {/* {cert.type !== "revoke" && (
          <Tooltip title="Bằng cấp hợp lệ, sẵn sàng để chia sẻ">
            <CheckIcon color="primary" size="1rem"></CheckIcon>
          </Tooltip>
        )}
        {!cert.type === "revoke" && (
          <Tooltip title="Bằng cấp đã bị thu hồi!">
            <ErrorOutlineIcon color="secondary" size="1rem"></ErrorOutlineIcon>
          </Tooltip>
        )} */}
            </Box>
            <Divider></Divider>
            <Grid container>
                <Grid item sm={12} md={6}>
                    <SimpleTable rows={certPart1}></SimpleTable>
                </Grid>
                <Grid item sm={12} md={6}>
                    <SimpleTable rows={certPart2}></SimpleTable>
                </Grid>
            </Grid>
        </>
    );
}

function SimpleTable({ rows }) {
    return (
        <TableContainer>
            <Table size="small">
                <TableBody>
                    {Object.entries(rows).map((entry, index) => (
                        <TableRow key={index}>
                            <TableCell style={{ width: "50%" }}>{entry[0]}</TableCell>
                            <TableCell>{entry[1]}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
}

function separateCertificate(cert) {
    //   const link = getLinkFromTxid(cert.txid);
    let certPart1 = {
        "Họ và tên": cert.student_name,
        // "Ngày sinh": plain.birthday,
        // "Giới tính": plain.gender,
        Trường: cert.university_name,
        "Ngành học": cert.major,
        // "Loại bằng": cert.,
        "Năm tốt nghiệp": cert.grad_year,
    };
    let certPart2 = {
        "Xếp loại": cert.certificate_level,
        "Hình thức đào tạo": cert.education_form,
        CPA: cert.cpa,
        "Ngày cấp": cert.timestamp,
        // "Hiệu trưởng": plain.headmaster,
        // "Số hiệu": plain.regisno,
        // "Số hiệu vào sổ": plain.globalregisno,
        Txid: cert.create_txid,
    };
    return [certPart1, certPart2];
}

// const certPart1 = {
//   "Họ và tên": "Nguyễn Văn An",
//   "Ngày sinh": "01/01/1998",
//   "Nơi sinh": "Từ Sơn, Bắc Ninh",
//   "Giới tính": "Nam",
//   "Dân tộc": "Kinh",
//   "Học sinh trường": "Trung học cơ sở Hương Mạc I",
//   "Năm tốt nghiệp": "2016",
// };

// const certPart2 = {
//   "Xếp loại tốt nghiệp": "Khá",
//   "Hình thức đào tạo": "Chính quy",
//   "Số hiệu": "A09050634",
//   "Số vào sổ cấp bằng": "185",
//   "Trưởng phòng GD&ĐT": "Nguyễn Văn Bình",
//   Txid: "2443d2798645516f6d985347ba456ce6da416063952565d0a33d0d2009ee7a3f".substr(0, 20),
// };
