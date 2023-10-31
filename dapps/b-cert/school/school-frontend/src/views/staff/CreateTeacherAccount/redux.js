const { createSlice } = require("@reduxjs/toolkit");

const teacherSlice = createSlice({
    name: "teacherSlice",
    initialState: { fetching: true, professors: [], uploading: false, reload_table: true }, // professors item: {time: "01/01/2020", profiles:[{teacherId, name, email, department, publicKey, firstTimePassword}] }
    reducers: {
        setPreloadProfessors: (state, action) => {
            state.fetching = false;
            state.professors = action.payload;
        },
        startUploadFile: (state, action) => {
            state.uploading = true;
        },
        uploadFileSuccess: (state) => {
            state.uploading = false;
            state.reload_table = !state.reload_table;
        },
        uploadFileFail: (state, action) => {
            state.uploading = false;
        },
    },
});

export default teacherSlice.reducer;
export const { setPreloadProfessors, startUploadFile, uploadFileSuccess, uploadFileFail } = teacherSlice.actions;
