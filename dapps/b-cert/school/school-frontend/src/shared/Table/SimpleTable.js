import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from "@material-ui/core";
import PerfectScrollbar from "react-perfect-scrollbar";

export default function SimpleTable({ head, body, minWidth }) {
  return (
    <TableContainer>
      <PerfectScrollbar style={{ paddingBottom: minWidth ? "24px" : 0 }}>
        <Table size="small" style={{ minWidth }}>
          <TableHead>
            <TableRow>
              {head.map((columnTitle, index) => (
                <TableCell key={index}>{columnTitle}</TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {body.map((row, rowIndex) => (
              <TableRow key={rowIndex}>
                {row.map((cell, index) => (
                  <TableCell key={index}>{cell}</TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </PerfectScrollbar>
    </TableContainer>
  );
}
