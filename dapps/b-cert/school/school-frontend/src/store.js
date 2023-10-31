import { combineReducers, configureStore } from "@reduxjs/toolkit";
import profileReducer from "src/views/staff/Register/redux";
// import votingReducer from "src/views/staff//Voting/redux";
// import bureauReducer from "src/views/staff/CreateBureauAccount/redux";
import teacherReducer from "src/views/staff/CreateTeacherAccount/redux";
import teacherProfileReducer from "src/views/teacher/Profile/redux";
import studentReducer from "src/views/staff/CreateStudentAccount/redux";
import subjectReducer from "src/views/staff/UploadSubject/redux";
import classReducer from "src/views/staff/UploadClass/redux";
import certificateReducer from "src/views/staff/UploadCertificate/redux";
import revokeCertificateReducer from "src/views/staff/RevokeCertificate/redux";

export const resetStore = () => {
  return {
    type: "RESET_STORE",
  };
};

const rootReducer = (state, action) => {
  if (action.type === "RESET_STORE") {
    state = undefined;
  }
  return appReducer(state, action);
};

const appReducer = combineReducers({
  profileSlice: profileReducer,
//   votingSlice: votingReducer,
  // bureauSlice: bureauReducer,
  teacherSlice: teacherReducer,
  studentSlice: studentReducer,
  subjectSlice: subjectReducer,
  classSlice: classReducer,
  certificateSlice: certificateReducer,
  teacherProfileSlice: teacherProfileReducer,
  revokeCertificateSlice: revokeCertificateReducer,
});

export default configureStore({
  reducer: rootReducer,
});
