import axios from "axios";
import { ACCOUNT_SERVICE_URL } from "src/constant/config";
import { getToken } from "src/utils/token";

export async function login(params) {
    const response = await axios({
        method: "post",
        url: `${ACCOUNT_SERVICE_URL}/login`,
        data: params,
        headers: {
            "Content-Type": "application/json",
        },
        timeout: 30000,
    });
    // localStorage.setItem("user", JSON.stringify(response.data.data.user));
    return response;
}

export async function getUserInfo(user_id) {
    const response = await axios({
        method: "GET",
        url: `${ACCOUNT_SERVICE_URL}/users/info`,
        headers: {
            "Content-Type": "application/json",
            Authorization: getToken(),
        },
        timeout: 30000,
    });
    return response;
}
