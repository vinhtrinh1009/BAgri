import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from "@material-ui/core";
import { getLinkFromTxid, toDateTimeString } from "../../../utils/utils";

export default function EditGradeHistory({ student }) {
  return (
    <>
      <Typography variant="h4">Lịch sử điểm</Typography>
      <TableContainer>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>#</TableCell>
              <TableCell>Điểm GK</TableCell>
              <TableCell>Điểm CK</TableCell>
              <TableCell>Thời gian</TableCell>
              <TableCell>Txid</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {student.versions.map((version, vIndex) => {
              return (
                <TableRow>
                  <TableCell>{vIndex + 1}</TableCell>
                  <TableCell>{version.halfSemesterPoint}</TableCell>
                  <TableCell>{version.finalSemesterPoint}</TableCell>
                  <TableCell>{toDateTimeString(version.timestamp)}</TableCell>
                  <TableCell>{getLinkFromTxid(version.txid, 20)}</TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>
    </>
  );
}
