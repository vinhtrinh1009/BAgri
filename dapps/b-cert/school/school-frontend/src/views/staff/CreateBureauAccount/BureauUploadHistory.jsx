import {
  Accordion,
  AccordionActions,
  AccordionDetails,
  AccordionSummary,
  Box,
  Button,
  Divider,
  makeStyles,
  Typography,
} from "@material-ui/core";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import GetAppIcon from "@material-ui/icons/GetApp";
import { useSnackbar } from "notistack";
import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getToken } from "src/utils/mng-token";
import XLSX from "xlsx";
import SimpleTable from "../../../shared/Table/SimpleTable";
import { ERR_TOP_CENTER } from "../../../utils/snackbar-utils";
import { getLinkFromTxid } from "../../../utils/utils";
import { setPreloadHistory } from "./redux";

const useStyles = makeStyles((theme) => ({
  root: {
    width: "100%",
  },
  heading: {
    fontSize: theme.typography.pxToRem(15),
    fontWeight: theme.typography.fontWeightRegular,
  },
}));

export default function BureauUploadHistory() {
  const cls = useStyles();
  const fetching = useSelector((state) => state.bureauSlice.fetching);
  const history = useSelector((state) => state.bureauSlice.history);
  const dp = useDispatch();
  const { enqueueSnackbar } = useSnackbar();

  useEffect(() => {
    fetchHistory();
  }, []);

  async function fetchHistory() {
    const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/v1.2/staff/bureau-history`, {
      headers: { Authorization: getToken() },
    });
    if (!response.ok) {
      enqueueSnackbar(`${response.status}: ${await response.text()}`, ERR_TOP_CENTER);
    } else {
      const result = await response.json();
      dp(setPreloadHistory(result));
    }
  }

  async function hdDownloadClick(e, item) {
    // let profiles = item.profiles.map((profile, index) => ({ 'Mã giáo vụ':  }));
    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.json_to_sheet(item.profiles);
    XLSX.utils.book_append_sheet(wb, ws, "Giáo vụ - " + item.time);
    XLSX.writeFile(wb, "giao-vu-" + item.time + ".xlsx");
  }

  const head = ["Mã giáo vụ", "Họ và tên", "Bộ môn", "Account", "Password", "Txid"];
  const title = "Lịch sử upload Giáo vụ";
  const content = (
    <Box>
      {history.map((item, index) => {
        const body = item.profiles.map((profile) => [
          profile.bureauId,
          profile.name,
          profile.department,
          profile.email,
          profile.firstTimePassword,
          getLinkFromTxid(profile.txid),
        ]);
        return (
          <Accordion key={index}>
            <AccordionSummary expandIcon={<ExpandMoreIcon />} id={item._id} className={cls.summary}>
              <Typography className={cls.heading}>{`#${index + 1}, ${item.time}`}</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <SimpleTable title={title} head={head} body={body}></SimpleTable>
            </AccordionDetails>
            <Divider />
            <AccordionActions>
              <Button startIcon={<GetAppIcon />} variant="outlined" color="primary" onClick={(e) => hdDownloadClick(e, item)}>
                Download
              </Button>
            </AccordionActions>
          </Accordion>
        );
      })}
    </Box>
  );
  return fetching ? null : content;
}
