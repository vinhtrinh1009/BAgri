import { makeStyles } from "@material-ui/core";
import BarForShareButton from "./BarForShareButton";
import DecryptedCertInfo from "./DecryptedCertInfo";
// import DecryptedSubjectTable from "./DecryptedSubjectTable";

const useStyels = makeStyles((theme) => ({
  root: {
    "& > *": {
      margin: theme.spacing(2, 0),
    },
  },
}));

export default function ShowDecryptInfo(props) {
  const cls = useStyels();

  return (
    <div className={cls.root}>
      <BarForShareButton></BarForShareButton>
      <DecryptedCertInfo></DecryptedCertInfo>
      {/* <DecryptedSubjectTable></DecryptedSubjectTable> */}
    </div>
  );
}
