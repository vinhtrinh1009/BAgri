const { createSlice } = require("@reduxjs/toolkit");

const studentSlice = createSlice({
    name: "studentSlice",
    initialState: { fetching: true, students: [], uploading: false, reload_table: true }, // students item: {time: "01/01/2020", profiles:[{studentId, name, email, department, publicKey, firstTimePassword}] }
    reducers: {
        setPreloadStudents: (state, action) => {
            state.fetching = false;
            state.students = action.payload;
        },
        startUploadFile: (state, action) => {
            state.uploading = true;
        },
        uploadFileSuccess: (state, action) => {
            state.uploading = false;
            state.reload_table = !state.reload_table;
        },
        uploadFileFail: (state, action) => {
            state.uploading = false;
        },
    },
});

export default studentSlice.reducer;
export const { setPreloadStudents, startUploadFile, uploadFileSuccess, uploadFileFail } = studentSlice.actions;
