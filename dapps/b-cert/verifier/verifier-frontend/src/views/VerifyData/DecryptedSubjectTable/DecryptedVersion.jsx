import { CircularProgress, TableCell, TableRow } from "@material-ui/core";
import { getLinkFromTxid } from "../../../utils/utils";
import CheckIcon from "@material-ui/icons/Check";
import CloseIcon from "@material-ui/icons/Close";
import { useEffect, useState } from "react";
import axios from "axios";
import { ERR_TOP_CENTER } from "../../../utils/snackbar-utils";
import { useSnackbar } from "notistack";
import { useSelector } from "react-redux";

export default function DecryptedVersion({ subjectIndex, version, versionIndex }) {
  const versionBKC = useSelector((state) => state.appSlice.eduProgramOnBKC.subjects[subjectIndex].versions[versionIndex]);
  const [isIntegrity, setIsIntegrity] = useState(null);
  const { enqueueSnackbar } = useSnackbar();

  useEffect(() => {
    checkIntegrity();
  }, []);

  async function checkIntegrity() {
    try {
      const response = await axios.post("/check-integrity", {
        hash: versionBKC.hash,
        plain: version.plain,
      });
      setIsIntegrity(response.data.isIntegrity);
    } catch (error) {
      enqueueSnackbar(JSON.stringify(error.response.data), ERR_TOP_CENTER);
    }
  }

  return (
    <TableRow>
      <TableCell>{version.plain.semester}</TableCell>
      <TableCell>{version.plain.subject.subjectId}</TableCell>
      <TableCell>{version.plain.subject.subjectName}</TableCell>
      <TableCell>{version.plain.subject.credit}</TableCell>
      <TableCell>{version.plain.halfSemesterPoint}</TableCell>
      <TableCell>{version.plain.finalSemesterPoint}</TableCell>
      <TableCell>{version.plain.teacherId}</TableCell>
      <TableCell>{version.plain.teacherName}</TableCell>
      <TableCell>{getLinkFromTxid(version.txid, 10)}</TableCell>
      <TableCell align="center">
        {isIntegrity === null && <CircularProgress size="1rem" />}
        {isIntegrity === true && <CheckIcon color="primary" />}
        {isIntegrity === false && <CloseIcon color="secondary" />}
      </TableCell>
    </TableRow>
  );
}
