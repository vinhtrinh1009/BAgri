import { UPDATE_PROFILE_FAIL } from "src/redux/Guest/actionTypes";
import { UPDATE_PROFILE } from "./actionTypes";
import { UPDATE_EMAIL } from "./actionTypes";
import { UPDATE_EMAIL_FAIL } from "./actionTypes";
import { UPDATE_PASSWORD_SUCCESSFUL } from "./actionTypes";
import { LOGOUT } from "./actionTypes";
import { SEND_VERIFY_SUCCESSFUL } from "./actionTypes";
import { VERIFY_PASSWORD } from "./actionTypes";
import { VERIFY_EMAIL_SUCCESSFUL } from "./actionTypes";
import { VERIFY_EMAIL } from "./actionTypes";
import { SEND_VERIFY_FAIL } from "./actionTypes";
import { SEND_VERIFY } from "./actionTypes";
import { UPDATE_PASSWORD_FAIL } from "./actionTypes";
import { UPDATE_PASSWORD } from "./actionTypes";
import { UPDATE_EMAIL_SUCCESSFUL } from "./actionTypes";
import { ALERT_SETTING } from "./actionTypes";
import { UPDATE_PROFILE_SUCCESSFUL } from "./actionTypes";
import { PROFILE } from "./actionTypes";
import { CATEGORY } from "./actionTypes";

const initial_state = {
    category: "account",
    profile: "",
    alert: "",
    logout: false,
    verify_email: null,
};

export default (state = initial_state, action) => {
    switch (action.type) {
        case CATEGORY:
            return { ...state, category: action.payload };
        case PROFILE:
            return { ...state, profile: action.payload };
        case UPDATE_PROFILE_FAIL:
            return {
                ...state,
                alert: {
                    color: "fail",
                    open: true,
                    message: action.payload,
                    time: 3000,
                },
            };
        case ALERT_SETTING:
            return {
                ...state,
                alert: action.payload,
            };

        case UPDATE_PASSWORD_SUCCESSFUL:
            return { ...state, logout: action.payload };
        case VERIFY_EMAIL_SUCCESSFUL:
            return { ...state, verify_email: action.payload };
        default:
            return { ...state };
    }
};

export const settingActions = {
    updateProfile: (params) => ({ type: UPDATE_PROFILE, payload: params }),
    updateProfileSuccessful: (params) => ({ type: UPDATE_PROFILE_SUCCESSFUL, payload: params }),
    updateProfileFail: (params) => ({ type: UPDATE_PROFILE_FAIL, payload: params }),
    updateEmail: (params) => ({ type: UPDATE_EMAIL, payload: params }),
    updateEmailSuccessful: (params) => ({ type: UPDATE_EMAIL_SUCCESSFUL, payload: params }),
    updateEmailFail: (params) => ({ type: UPDATE_EMAIL_FAIL, payload: params }),
    updatePassword: (params) => ({ type: UPDATE_PASSWORD, payload: params }),
    updatePasswordSuccessful: (params) => ({ type: UPDATE_PASSWORD_SUCCESSFUL, payload: params }),
    updatePasswordFail: (params) => ({ type: UPDATE_PASSWORD_FAIL, payload: params }),
    sendVerifyPassword: (params) => ({ type: SEND_VERIFY, payload: params }),
    sendVerifyPasswordSuccessful: (params) => ({ type: SEND_VERIFY_SUCCESSFUL, payload: params }),
    sendVerifyPasswordFail: (params) => ({ type: SEND_VERIFY_FAIL, payload: params }),
    verifyPassword: (params) => ({ type: VERIFY_PASSWORD, payload: params }),
    verifyEmail: (params) => ({ type: VERIFY_EMAIL, payload: params }),
    verifyEmailSuccessful: (params) => ({ type: VERIFY_EMAIL_SUCCESSFUL, payload: params }),
};
