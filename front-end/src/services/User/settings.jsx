import axios from "axios";
import { ACCOUNT_SERVICE_URL, ACCOUNT_SERVICE_URL_DEV } from "src/constant/config";
import { getToken } from "src/utils/token";

export async function updateProfile(payload) {
    const response = await axios({
        method: "PUT",
        url: `${ACCOUNT_SERVICE_URL}/users/${payload.user_id}`,
        headers: {
            "Content-Type": "application/json",
            Authorization: getToken(),
        },
        data: payload.data,
        timeout: 30000,
    });
    return response;
}

export async function updatePassword(payload) {
    const response = await axios({
        method: "PUT",
        url: `${ACCOUNT_SERVICE_URL}/users/${payload.user_id}/change_password`,
        headers: {
            "Content-Type": "application/json",
            Authorization: getToken(),
        },
        data: payload.data,
        timeout: 30000,
    });
    return response;
}
export async function sendVerify(payload) {
    const response = await axios({
        method: "PUT",
        url: `${ACCOUNT_SERVICE_URL}/users/${payload.user_id}/send_verify`,
        headers: {
            "Content-Type": "application/json",
            Authorization: getToken(),
        },
        data: payload.data,
        timeout: 30000,
    });
    return response;
}
export async function verifyPassword(payload) {
    const response = await axios({
        method: "PUT",
        url: `${ACCOUNT_SERVICE_URL}/users/${payload.user_id}/verify/password`,
        headers: {
            "Content-Type": "application/json",
            Authorization: getToken(),
        },
        data: payload,
        timeout: 30000,
    });
    return response;
}
export async function verifyEmail(payload) {
    const response = await axios({
        method: "PUT",
        url: `${ACCOUNT_SERVICE_URL}/users/${payload.user_id}/verify/email`,
        headers: {
            "Content-Type": "application/json",
            Authorization: getToken(),
        },
        data: payload,
        timeout: 30000,
    });
    return response;
}
