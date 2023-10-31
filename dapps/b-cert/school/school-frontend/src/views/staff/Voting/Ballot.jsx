import { Box, Collapse } from "@material-ui/core";
import BallotBody from "src/shared/BallotBody";
import BallotHeader from "./BallotHeader";

export default function Ballot({ ballot }) {
  return (
    <Collapse in={ballot.in ?? true} collapsedHeight={0}>
      <Box mb={3}>
        <BallotHeader ballot={ballot}></BallotHeader>
        <BallotBody ballot={ballot}></BallotBody>
      </Box>
    </Collapse>
  );
}
