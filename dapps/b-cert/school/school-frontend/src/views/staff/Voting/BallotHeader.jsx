import { Avatar, Box, Button, Typography } from "@material-ui/core";
import axios from "axios";
import { useSnackbar } from "notistack";
import { useDispatch } from "react-redux";
import { requirePrivateKeyHex } from "../../../utils/keyholder";
import { ERR_TOP_CENTER, SUCCESS_BOTTOM_CENTER } from "../../../utils/snackbar-utils";
import { collapseBallot } from "./redux";

export default function BallotHeader({ ballot }) {
  const dp = useDispatch();
  const { enqueueSnackbar } = useSnackbar();

  async function hdVote(decision, requesterPublicKey) {
    const privateKeyHex = await requirePrivateKeyHex(enqueueSnackbar);
    try {
      const response = await axios.post("/staff/vote", { decision, requesterPublicKey, privateKeyHex });
      dp(collapseBallot({ publicKey: requesterPublicKey }));
      enqueueSnackbar("Đã bỏ phiếu xong!", SUCCESS_BOTTOM_CENTER);
    } catch (error) {
      console.error(error);
      if (error.response) enqueueSnackbar(JSON.stringify(error.response.data), ERR_TOP_CENTER);
    }
  }

  return (
    <div>
      <Box bgcolor="white" px={2} py={1} display="flex" alignItems="center">
        <Box flexGrow={1} display="flex" alignItems="center">
          <Avatar src={ballot.imgSrc}></Avatar>
          <Box mx={2}>
            <Typography variant="h5">{ballot.universityName}</Typography>
          </Box>
        </Box>
        <Box pr={2} flexShrink={0}>
          <Button variant="contained" color="primary" onClick={(e) => hdVote("accept", ballot.publicKey)}>
            Đồng ý
          </Button>
        </Box>
        <Box flexShrink={0}>
          <Button onClick={(e) => hdVote("decline", ballot.publicKey)}>Từ chối</Button>
        </Box>
      </Box>
    </div>
  );
}
