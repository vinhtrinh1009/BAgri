const { createSlice } = require("@reduxjs/toolkit");

const sawtoothAccountsSlice = createSlice({
  name: "sawtoothAccountsSlice",
  initialState: { fetching: true, accounts: [] },
  reducers: {
    setFetchedAccounts: (state, action) => {
      state.fetching = false;
      state.accounts = action.payload;
    },
    addSawtoothAccount: (state, action) => {
      let newAcc = action.payload;
      if (newAcc.privateKeyHex === "") {
        newAcc.privateKeyHex = false;
      }
      state.accounts.push(newAcc);
    },
    deleteSawtoothAccount: (state, action) => {
      state.accounts = state.accounts.filter((acc) => acc.publicKeyHex !== action.payload.publicKeyHex);
    },
  },
});

export default sawtoothAccountsSlice.reducer;
export const { setFetchedAccounts, addSawtoothAccount, deleteSawtoothAccount } = sawtoothAccountsSlice.actions;
