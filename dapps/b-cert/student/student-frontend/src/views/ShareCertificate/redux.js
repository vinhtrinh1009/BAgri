const { createSlice } = require("@reduxjs/toolkit");

const initState = {
//   selectedAccount: null,
  eduProgram: {
      'university': [], 
      'edu_program': []
  },
  certificateData: [],
  encryptData: [],
  show: "none", // none, encrypt, decrypt
  loading: true
};

const shareCertificateSlice = createSlice({
  name: "shareCertificateSlice",
  initialState: initState,
  reducers: {
    // deselectAccount: (state, action) => {
    //   Object.assign(state, initState);
    // },
    // setSelectedAccAndEduPrograms: (state, action) => {
    //   state.selectedAccount = action.payload.selectedAccount;
    //   state.eduPrograms = action.payload.eduPrograms;
    // },
    // setSelectedEduProgram: (state, action) => {
    //   state.selectedEduProgram = action.payload.selectedEduProgram;
    //   state.show = "encrypt";
    // },
    // deselectEduProgram: (state, action) => {
    //   state.selectedEduProgram = null;
    //   state.show = "none";
    // },

    setEduProgram: (state, action) => {
        state.eduProgram.university = action.payload.user.university
        state.eduProgram.edu_program = action.payload.education_form
    },
    setCertificateData: (state, action) => {
      state.certificateData = action.payload;
      state.show = "decrypt";
      state.loading = false
    },
    setEncryptData: (state, action) => {
        state.encryptData = action.payload
        state.show = "encrypt"
    }
  },
});

export default shareCertificateSlice.reducer;
export const {
  setEduProgram,
  setCertificateData,
  setEncryptData
} = shareCertificateSlice.actions;
