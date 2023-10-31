import { configureStore } from "@reduxjs/toolkit";
import appReducer from "./views/redux";

export default configureStore({
  reducer: { appSlice: appReducer },
});
