import { Box, Grid } from "@material-ui/core";
import { useSelector } from "react-redux";
import Page from "src/shared/Page";
import AvatarBar from "./AvatarBar";
import ProfileForm from "./ProfileForm";
import VotingState from "./VotingState";

export default function MakeRequest() {
  const votingState = useSelector((state) => state.profileSlice.state);
  return (
    <Page title="Đăng kí tham gia">
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <ProfileForm></ProfileForm>
        </Grid>
        <Grid item xs={12} md={4}>
          <AvatarBar></AvatarBar>
          <Box mt={2}>
            {(votingState === "voting" || votingState === "accepted" || votingState === "declined") && <VotingState></VotingState>}
          </Box>
        </Grid>
      </Grid>
    </Page>
  );
}
