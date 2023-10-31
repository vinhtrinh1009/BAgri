import { makeStyles, Typography } from "@material-ui/core";
import { useSelector } from "react-redux";
import Page from "src/shared/Page";
import Ballots from "./Ballots";

const useStyles = makeStyles((theme) => ({
  flexContainer: {
    height: "100%",
    width: "100%",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
  },
}));
export default function Voting(props) {
  const cls = useStyles();
  const registrationState = useSelector((state) => state.profileSlice.state);

  return (
    <Page title="Bỏ phiếu">
      {registrationState === "accepted" ? (
        <Ballots></Ballots>
      ) : (
        <div className={cls.flexContainer}>
          <Typography variant="h3">Hiện tại bạn chưa thể thực hiện bỏ phiếu!</Typography>
          <Typography variant="subtitle1">Sau khi tham gia thành công bạn sẽ có thể thực hiện bỏ phiếu.</Typography>
        </div>
      )}
    </Page>
  );
}
