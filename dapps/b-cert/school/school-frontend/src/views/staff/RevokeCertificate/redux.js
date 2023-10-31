const { createSlice } = require("@reduxjs/toolkit");

const revokeCertificateSlice = createSlice({
  name: "revokeCertificateSlice",
  initialState: { document: null },
  reducers: {
    setDocument: (state, action) => {
      state.document = action.payload;
    },
  },
});

export default revokeCertificateSlice.reducer;
export const { setDocument } = revokeCertificateSlice.actions;
