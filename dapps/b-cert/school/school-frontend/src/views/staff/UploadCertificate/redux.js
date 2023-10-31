const { createSlice } = require("@reduxjs/toolkit");

const certificateSlice = createSlice({
  name: "certificateSlice",
  initialState: { fetching: true, docs: [], uploading: false },
  reducers: {
    setPreloadCertDocuments: (state, action) => {
      state.fetching = false;
      if (action.payload.length > 0) state.docs = action.payload;
    },
    startUploadFile: (state, action) => {
      state.uploading = true;
    },
    uploadFileSuccess: (state, action) => {
      state.uploading = false;
      state.docs = [];
      state.docs = action.payload.concat(state.docs);
    },
    uploadFileFail: (state, action) => {
      state.uploading = false;
    },
  },
});

export default certificateSlice.reducer;
export const { setPreloadCertDocuments, startUploadFile, uploadFileSuccess, uploadFileFail } = certificateSlice.actions;
