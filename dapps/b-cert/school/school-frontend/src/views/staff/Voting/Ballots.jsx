import { Box, Typography } from "@material-ui/core";
import axios from "axios";
import { useSnackbar } from "notistack";
import { useCallback, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { ERR_TOP_CENTER } from "../../../utils/snackbar-utils";
import Ballot from "./Ballot";
import { setBallots } from "./redux";

export default function Ballots(props) {
  const loading = useSelector((state) => state.votingSlice.fetching);
  const ballots = useSelector((state) => state.votingSlice.ballots);
  const numOfNewBallot = useSelector((state) => state.votingSlice.numOfNewBallot);

  const dp = useDispatch();
  const { enqueueSnackbar } = useSnackbar();

  // make thing complicated just for remove warning on useEffect :v
  const fetchNewBallots = useCallback(async () => {
    try {
      const response = await axios.get("/staff/ballots?state=new");
      dp(setBallots(response.data));
    } catch (error) {
      console.error(error);
      if (error.response) enqueueSnackbar(JSON.stringify(error.response.data), ERR_TOP_CENTER);
    }
  }, [dp, enqueueSnackbar]);

  useEffect(() => {
    fetchNewBallots();
  }, [fetchNewBallots]);

  useEffect(() => {
    const clockId = setInterval(() => {
      fetchNewBallots();
    }, 3000);
    return () => {
      window.clearInterval(clockId);
    };
  });

  let content =
    numOfNewBallot > 0 ? (
      ballots.map((ballot, index) => <Ballot ballot={ballot} key={index}></Ballot>)
    ) : (
      <Box py={2} mb={3} bgcolor="white">
        <Typography variant="h4" align="center">
          Chưa có thêm yêu cầu bỏ phiếu mới nào!
        </Typography>
      </Box>
    );

  return <div>{loading ? null : content}</div>;
}
