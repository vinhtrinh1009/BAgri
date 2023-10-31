import { Avatar, Box, makeStyles, Paper, Table, TableBody, TableCell, TableContainer, TableRow, Typography } from "@material-ui/core";
import CheckIcon from "@material-ui/icons/Check";
import CloseIcon from "@material-ui/icons/Close";
import DoneAllIcon from "@material-ui/icons/DoneAll";
import HowToVoteIcon from "@material-ui/icons/HowToVote";
import axios from "axios";
import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { updateVotingState } from "./redux";

const useStyles = makeStyles((theme) => ({
  root: {
    "& .MuiTableCell-sizeSmall": {
      padding: theme.spacing(1),
    },
  },
  head: {
    width: "95%",
    margin: "auto",
    padding: theme.spacing(2.5, 2),
    backgroundColor: (props) => {
      if (props.votingState === "voting") return theme.palette.info.main;
      else if (props.votingState === "accepted") return theme.palette.success.main;
      else if (props.votingState === "declined") return theme.palette.error.main;
      else return theme.palette.primary.main;
    },
    color: "white",
    position: "relative", // this bring head foreground
  },
  body: { width: "100%", marginTop: "-32px", padding: theme.spacing(6, 2, 2, 2) },
}));

export default function VotingState(props) {
  const votingState = useSelector((state) => state.profileSlice.state);
  const votes = useSelector((state) => state.profileSlice.votes);
  const cls = useStyles({ votingState });
  const dp = useDispatch();

  // interval update voting state! (y), so professional!
  useEffect(() => {
    if (votingState === "voting") {
      const clockId = setInterval(async () => {
        try {
          const response = await axios.get("/staff/my-university-profile");
          dp(updateVotingState(response.data));
        } catch (error) {
          console.error(error);
        }
      }, 3000);
      return () => {
        window.clearInterval(clockId);
      };
    }
  });

  return (
    <div>
      <Box className={cls.root}>
        <Paper className={cls.head}>
          <Typography variant="h3">
            {votingState === "voting" && (
              <>
                Đang bỏ phiếu <HowToVoteIcon></HowToVoteIcon>
              </>
            )}
            {votingState === "accepted" && (
              <>
                Đã tham gia <DoneAllIcon></DoneAllIcon>
              </>
            )}
            {votingState === "declined" && (
              <>
                Đã bị từ chối <CloseIcon></CloseIcon>
              </>
            )}
          </Typography>
        </Paper>
        <Paper className={cls.body}>
          <TableContainer>
            <Table size="small">
              <TableBody>
                {votes &&
                  votes.map((vote, index) => (
                    <TableRow key={index}>
                      <TableCell>
                        <Avatar src={vote.imgSrc}></Avatar>
                      </TableCell>
                      <TableCell>{vote.isMinistry ? vote.name : vote.universityName}</TableCell>
                      <TableCell>
                        {vote.decision === "accept" && <CheckIcon color="primary"></CheckIcon>}
                        {vote.decision === "decline" && <CloseIcon color="secondary"></CloseIcon>}
                      </TableCell>
                      <TableCell>
                        <i>
                          <small>{vote.time}</small>
                        </i>
                      </TableCell>
                    </TableRow>
                  ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      </Box>
    </div>
  );
}
