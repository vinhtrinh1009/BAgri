import Paper from "@material-ui/core/Paper";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableRow from "@material-ui/core/TableRow";

// table show school info
export default function BallotBody({ ballot }) {
  return (
    <div>
      <TableContainer component={Paper}>
        <Table size="small">
          <TableBody>
            <TableRow>
              <TableCell>Tên Tiếng Anh</TableCell>
              <TableCell>{ballot.nameInEnglish}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Địa chỉ</TableCell>
              <TableCell>{ballot.address}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Email</TableCell>
              <TableCell>{ballot.email}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Số điện thoại</TableCell>
              <TableCell>{ballot.phone}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Public key</TableCell>
              <TableCell>{ballot.publicKey}</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
}
