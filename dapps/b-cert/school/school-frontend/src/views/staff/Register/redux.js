import { createSlice } from "@reduxjs/toolkit";

export const profileSlice = createSlice({
    name: "profileSlice",
    initialState: {
        fetching: true,
        id: "",
        university_name: "",
        nameInEnglish: "",
        address: "",
        email: "",
        phone: "",
        public_key: "",
        description: "",
        avatar: null,
        state: false,
        reload: false,
    }, // votes filed too
    reducers: {
        setProfile: (state, action) => {
            state.fetching = false;
            Object.assign(state, action.payload);
            state.state = action.payload.status;
        },
        setReload: (state) => {
            state.reload = !state.reload;
        },
        updateImgSrc: (state, action) => {
            state.avatar = action.payload;
        },
        updateVotingState: (state, action) => {
            if (state.state !== action.payload.status) state.state = action.payload.status;
        },
    },
});

export const { setProfile, updateImgSrc, updateVotingState, setReload } = profileSlice.actions;
export default profileSlice.reducer;
