import { createSlice } from "@reduxjs/toolkit";

const votingSlice = createSlice({
  name: "votingSlice",
  initialState: { fetching: true, ballots: [], numOfNewBallot: 0, privateKey: null }, // dont remove numOfNewBallot, it is difference from ballots.length
  reducers: {
    setBallots: (state, action) => {
      state.fetching = false;
      state.ballots = action.payload;
      state.numOfNewBallot = action.payload.length;
    },
    collapseBallot(state, action) {
      const index = state.ballots.findIndex((ballot) => ballot.publicKey === action.payload.publicKey);
      state.ballots[index].in = false;
      state.numOfNewBallot -= 1;
    },
  },
});

export default votingSlice.reducer;
export const { setBallots, removeVotedRequest, collapseBallot } = votingSlice.actions;
