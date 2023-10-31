import EncryptedCertInfo from "./EncryptedCertInfo";
import EncryptedSubjectTable from "./EncryptedSubjectTable";
import BarForDecryptButton from "./BarForDecryptButton";
import { makeStyles } from "@material-ui/core";

const useStyels = makeStyles((theme) => ({
  root: {
    "& > *": {
      margin: theme.spacing(2, 0),
    },
  },
}));

export default function ShowEncryptedInfo(props) {
  const cls = useStyels();

  return (
    <div className={cls.root}>
      <BarForDecryptButton></BarForDecryptButton>
      <EncryptedCertInfo></EncryptedCertInfo>
      <EncryptedSubjectTable></EncryptedSubjectTable>
    </div>
  );
}
