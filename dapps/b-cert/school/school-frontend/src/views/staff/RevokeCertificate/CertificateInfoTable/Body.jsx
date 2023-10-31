import { Grid, Table, TableBody, TableCell, TableContainer, TableRow } from "@material-ui/core";
import React from "react";
import { getLinkFromTxid } from "src/utils/utils";

export default function Body({ cert }) {
  const [certPart1, certPart2] = separateCertificate(cert);
  return (
    <Grid container>
      <Grid item sm={12} md={6}>
        <SimpleTable rows={certPart1}></SimpleTable>
      </Grid>
      <Grid item sm={12} md={6}>
        <SimpleTable rows={certPart2}></SimpleTable>
      </Grid>
    </Grid>
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
    "Trường": cert.university_name,
    "Ngành học": cert.student_major,
    // "Loại bằng": cert.,
    "Năm tốt nghiệp": cert.grad_year,
  };
  let certPart2 = {
    "Xếp loại": cert.certificate_level,
    "Hình thức đào tạo": cert.education_form,
    "CPA": cert.cpa,
    "Ngày cấp": cert.timestamp,
    // "Hiệu trưởng": plain.headmaster,
    "Số hiệu": cert.register_id,
    // "Số hiệu vào sổ": plain.globalregisno,
    "Txid": cert.create_txid,
  };
  return [certPart1, certPart2];
  return [certPart1, certPart2];
}
