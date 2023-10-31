import { createSlice } from "@reduxjs/toolkit";

export const studentProfileSlice = createSlice({
  name: "studentProfileSlice",
  initialState: { fetching: true },
  reducers: {
    setProfile: (state, action) => {
      Object.assign(state, action.payload);
      state.fetching = false;
    },
    updateImgSrc: (state, action) => {
      state.imgSrc = action.payload;
    },
  },
});

export const { setProfile, updateImgSrc } = studentProfileSlice.actions;
export default studentProfileSlice.reducer;
