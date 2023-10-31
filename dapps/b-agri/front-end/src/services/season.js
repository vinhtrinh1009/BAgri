import { BAGRI_SERVICE_URL } from "src/constants/config";
import axios from "axios";

export async function getSeasonByID(payload) {
    const idSeason = payload["season_id"];
    const response = await axios({
        method: "GET",
        url: `${BAGRI_SERVICE_URL}/seasons/network/${payload}`,
        headers: {
            "Content-Type": "application/json"
        },
        timeout: 30000,
    }).catch((error) => {
        return { data: error.response };
        // { status: error.response.status, error: error.response.statusText } };
    });
    return response.data;
}
