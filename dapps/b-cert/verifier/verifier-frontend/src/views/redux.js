const { createSlice } = require("@reduxjs/toolkit");

const appSlice = createSlice({
    name: "appSlice",
    initialState: {
        loading: true,
    },
    reducers: {},
});

export default appSlice.reducer;
export const {} = appSlice.actions;
