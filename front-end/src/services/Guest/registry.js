import axios from "axios";
import { ACCOUNT_SERVICE_URL } from "src/constant/config";

export async function registry(params) {
    const response = await axios({
        method: 'post',
        url: `${ACCOUNT_SERVICE_URL}/users`,
        data: params,
        headers: {
            "Content-Type": "application/json"
        },
        timeout: 30000
    })
    return response
}