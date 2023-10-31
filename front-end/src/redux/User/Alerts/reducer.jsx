import { OPEN_CUSTOM_ALERT, OPEN_ERROR_ALERT, OPEN_INFO_ALERT, OPEN_SUCCESS_ALERT, OPEN_WARNING_ALERT, CLOSE_ALERT } from "./actionTypes";

export const alertType = { success: "success", info: "info", warning: "warning", error: "error" };
const initial_state = {
    open: false,
    autoHideDuration: 4000,
    alertType: "info",
    message: "",
};

export default (state = initial_state, action) => {
    switch (action.type) {
        case OPEN_CUSTOM_ALERT:
            return { ...state, ...action.payload, open: true };
        case OPEN_SUCCESS_ALERT:
            return { ...state, ...action.payload, open: true, autoHideDuration: 4000, alertType: alertType.success };
        case OPEN_ERROR_ALERT:
            return { ...state, ...action.payload, open: true, autoHideDuration: 4000, alertType: alertType.error };
        case OPEN_WARNING_ALERT:
            return { ...state, ...action.payload, open: true, autoHideDuration: 4000, alertType: alertType.warning };
        case OPEN_INFO_ALERT:
            return { ...state, ...action.payload, open: true, autoHideDuration: 4000, alertType: alertType.info };
        default:
            return { ...state, open: false };
    }
};

export const alertActions = {
    getAlert: () => ({ type: CLOSE_ALERT }),
};
