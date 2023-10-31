import { Box, Button, Collapse, Divider, IconButton, makeStyles, Paper, Typography } from "@material-ui/core";
import GetAppIcon from "@material-ui/icons/GetApp";
import SimpleTable from "../Table/SimpleTable";
import FileSaver from "file-saver";
import { useState } from "react";
import KeyboardArrowUpIcon from "@material-ui/icons/KeyboardArrowUp";
import KeyboardArrowDownIcon from "@material-ui/icons/KeyboardArrowDown";

const useStyles = makeStyles((theme) => ({

  button: {
    margin: theme.spacing(1),
  },
}));

export default function DownloadExampleData({ title, fileName, head, body, minWidth }) {
  const cls = useStyles();
  const [show, setShow] = useState(true);

  function hdClickDownload(e) {
    e.stopPropagation();
    FileSaver.saveAs(`/static/excels/${fileName}`, fileName);
  }

  function toggleCollapse() {
    setShow(!show);
  }

  return (
    <Paper>
      <Box
        pl={2}
        pr={1}
        display="flex"
        justifyContent="space-between"
        alignItems="center"
        onClick={toggleCollapse}
        style={{ cursor: "pointer", background:"#3f51b5", color:"white" }}
      >
        <Typography variant="h4">{title || "Mẫu dữ liệu"}</Typography>
        <Box>
          <IconButton onClick={hdClickDownload} style={{color: "white"}} title="Tải về">
            <GetAppIcon />
          </IconButton>
          {show ? (
            <IconButton onClick={toggleCollapse} style={{color: "white"}}>
              <KeyboardArrowUpIcon />
            </IconButton>
          ) : (
            <IconButton onClick={toggleCollapse} style={{color: "white"}}>
              <KeyboardArrowDownIcon />
            </IconButton>
          )}
        </Box>
      </Box>
      <Divider></Divider>
      <Collapse in={show}>
        <SimpleTable head={head} body={body} minWidth={minWidth}></SimpleTable>
      </Collapse>
    </Paper>
  );
}
