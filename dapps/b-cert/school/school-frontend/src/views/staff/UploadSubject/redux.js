const { createSlice } = require("@reduxjs/toolkit");

const subjectSlice = createSlice({
    name: "subjectSlice",
    initialState: { fetching: true, subjects: [], uploading: false, reload_table: true },
    reducers: {
        setPreloadSubjects: (state, action) => {
            state.fetching = false;
            // DataGrid need id field for display
            state.subjects = action.payload;
        },
        startUploadFile: (state, action) => {
            state.fetching = true;
        },
        uploadFileSuccess: (state, action) => {
            state.fetching = false;
            state.reload_table = !state.reload_table;
        },
        uploadFileFail: (state, action) => {
            state.fetching = false;
        },
    },
});

export default subjectSlice.reducer;
export const { setPreloadSubjects, startUploadFile, uploadFileSuccess, uploadFileFail } = subjectSlice.actions;
