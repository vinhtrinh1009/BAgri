const { createSlice } = require("@reduxjs/toolkit");

const classSlice = createSlice({
    name: "classSlice",
    initialState: { fetching: true, classes: [], uploading: false, shouldShowCaution: true, reload_table: true },
    reducers: {
        setPreloadClasses: (state, action) => {
            state.fetching = false;
            state.classes = action.payload;
        },
        setNewUploadClass: (state, action) => {
            state.new_upload = action.payload;
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
        setShouldShowCaution: (state, action) => {
            state.shouldShowCaution = action.payload;
        },
    },
});

export default classSlice.reducer;
export const { setPreloadClasses, startUploadFile, uploadFileSuccess, uploadFileFail, setShouldShowCaution } = classSlice.actions;
