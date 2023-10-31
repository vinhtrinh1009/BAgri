import { useNavigate } from "react-router";
import { takeEvery, put, call } from "redux-saga/effects";
import { UPDATE_PROFILE_SUCCESSFUL } from "src/redux/User/Settings/actionTypes";
import { UPDATE_PASSWORD } from "src/redux/User/Settings/actionTypes";
import { SEND_VERIFY } from "src/redux/User/Settings/actionTypes";
import { VERIFY_PASSWORD } from "src/redux/User/Settings/actionTypes";
import { VERIFY_EMAIL } from "src/redux/User/Settings/actionTypes";
import { UPDATE_EMAIL } from "src/redux/User/Settings/actionTypes";
import { UPDATE_PROFILE } from "src/redux/User/Settings/actionTypes";
import { settingActions } from "src/redux/User/Settings/reducer";
import { verifyEmail } from "src/services/User/settings";
import { verifyPassword } from "src/services/User/settings";
import { sendVerify } from "src/services/User/settings";
import { updatePassword } from "src/services/User/settings";
import { updateProfile } from "src/services/User/settings";
import { userActions } from "src/redux/Guest/reducer";

function* updateUserProfile({ payload }) {
    try {
        const response = yield call(updateProfile, payload);
        if (response.data.status == "success") {
            yield put(settingActions.updateProfileSuccessful(response.data.data));
            // localStorage.setItem("user", JSON.stringify(response.data.data.updated_user));
            yield put(userActions.getProfileSuccessful(response.data.data.updated_user));
            // window.location.reload();
        } else {
            yield put(settingActions.updateProfileFail(response.data));
            console.error(response);
        }
    } catch (error) {
        window.alert(error.response.data.error.message);
    }
}
function* updateEmail({ payload }) {
    try {
        const response = yield call(updateProfile, payload);
        if (response.data.status == "success") {
            yield put(settingActions.updateProfileSuccessful(response.data.data));
            // localStorage.setItem("user", JSON.stringify(response.data.data.updated_user));
            window.confirm("Please check your email for confirmation!");
        } else {
            yield put(settingActions.updateProfileFail(response.data));
            console.error(response);
        }
    } catch (error) {
        console.error(error);
    }
}
function* updateUserPassword({ payload }) {
    try {
        const response = yield call(updatePassword, payload);
        if (response.data.status == "success") {
            yield put(settingActions.updatePasswordSuccessful(true));
            localStorage.clear();
            window.alert("Update Password Successful!");
        } else {
            yield put(settingActions.updateProfileFail(response.data));
            console.error(response);
        }
    } catch (error) {
        console.error(error);
        window.alert(error.response.data.error.message);
    }
}
function* sendEmailVerify({ payload }) {
    try {
        const response = yield call(sendVerify, payload);
        if (response.data.status == "success") {
            yield put(settingActions.sendVerifyPasswordSuccessful(response.data.data));
            window.confirm("Please check your email for confirmation!");
        } else {
            yield put(settingActions.updateProfileFail(response.data));
        }
    } catch (error) {
        console.error(error);
        window.alert(error.response.data.error.message);
    }
}
function* verifyUserPassword({ payload }) {
    try {
        const response = yield call(verifyPassword, payload);
        if (response.data.status == "success") {
            yield put(settingActions.updatePasswordSuccessful(true));
            localStorage.clear();
            window.alert("Update Password Successful!");
        } else {
            yield put(settingActions.updateProfileFail(response.data));
        }
    } catch (error) {
        console.error(error);
        window.alert(error.response.data.error.message);
    }
}
function* verifyUserEmail({ payload }) {
    try {
        const response = yield call(verifyEmail, payload);
        if (response.data.status == "success") {
            yield put(settingActions.verifyEmailSuccessful(response.data));
            // localStorage.setItem("user", JSON.stringify(response.data.data.updated_user));
            window.alert("Verify Email Successful!");
            window.location.reload();
        } else {
            yield put(settingActions.updateProfileFail(response.data));
        }
    } catch (error) {
        console.error(error);
        window.alert(error.response.data.error.message);
    }
}
function* settingSagas() {
    yield takeEvery(UPDATE_PROFILE, updateUserProfile);
    yield takeEvery(UPDATE_EMAIL, updateEmail);
    yield takeEvery(UPDATE_PASSWORD, updateUserPassword);
    yield takeEvery(SEND_VERIFY, sendEmailVerify);
    yield takeEvery(VERIFY_PASSWORD, verifyUserPassword);
    yield takeEvery(VERIFY_EMAIL, verifyUserEmail);
}

export default settingSagas;
