import { Box, makeStyles, Paper, Typography } from "@material-ui/core";
import { Timeline, TimelineConnector, TimelineContent, TimelineDot, TimelineItem, TimelineSeparator } from "@material-ui/lab";
import { useSelector } from "react-redux";
import { toDateTimeString } from "../../../utils/utils";
import CertificateInfoTable from "./CertificateInfoTable";

const useStyles = makeStyles((theme) => ({
  root: {
    paddingLeft: 0,
    "& .MuiTimelineItem-missingOppositeContent:before": {
      flex: 0,
      padding: 0,
    },
  },
}));

export default function SearchResult(props) {
  const cls = useStyles();

  const document = useSelector((state) => state.revokeCertificateSlice.document);
  return (
    // <div>
    //   {document && (
    //     // <Paper>
    //     <Timeline align="left" className={cls.root}>
    //       <TimelineItem>
    //         <TimelineSeparator>
    //           <TimelineDot color={lastestVersion.type === "revoke" ? "secondary" : "primary"}></TimelineDot>
    //           <TimelineConnector></TimelineConnector>
    //         </TimelineSeparator>
    //         <TimelineContent>
    //           <Paper style={{ padding: 8 }}>
    //             <Typography>
    //               {`v${document.versions.length},${toDateTimeString(lastestVersion.timestamp)}: `}
    //               <strong>{lastestVersion.type === "revoke" && "Thu hồi"}</strong>
    //               <strong>{lastestVersion.type === "create" && "Cấp lần đầu"}</strong>
    //               <strong>{lastestVersion.type === "reactive" && "Cấp lại"}</strong>
    //             </Typography>
    //           </Paper>
    //           <Box mt={2}>
    //             <CertificateInfoTable cert={document.versions[document.versions.length - 1]}></CertificateInfoTable>
    //           </Box>
    //         </TimelineContent>
    //       </TimelineItem>
    //       {document.versions
    //         .slice(0, -1)
    //         .reverse()
    //         .map((version, index) => (
    //           <TimelineItem>
    //             <TimelineSeparator>
    //               <TimelineDot color={version.type === "revoke" ? "secondary" : "primary"}></TimelineDot>
    //               {index !== document.versions.length - 2 && <TimelineConnector></TimelineConnector>}
    //             </TimelineSeparator>
    //             <TimelineContent>
    //               <Paper style={{ padding: 8 }}>
    //                 <Typography>
    //                   {`v${version.version}, ${toDateTimeString(version.timestamp)}: `}
    //                   <strong>{version.type === "revoke" && "Thu hồi"}</strong>
    //                   <strong>{version.type === "create" && "Cấp lần đầu"}</strong>
    //                   <strong>{version.type === "reactive" && "Cấp lại"}</strong>
    //                 </Typography>
    //               </Paper>
    //             </TimelineContent>
    //           </TimelineItem>
    //         ))}
    //     </Timeline>
    //     // </Paper>
    //   )}
    // </div>
    <div>
        {document && (<CertificateInfoTable cert = {document}></CertificateInfoTable>)}
    </div>
    
  );
}
