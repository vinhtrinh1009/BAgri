import axios from "axios";
import { CORE_SERVICE_URL } from "src/constant/config";
import { getToken } from "src/utils/token";

export async function getDApps(params) {
    const response = await axios({
        method: "GET",
        url: `${CORE_SERVICE_URL}/dapps`,
        headers: {
            "Content-Type": "application/json",
            Authorization: getToken(),
        },
        timeout: 30000,
    });
    return response;
}

export async function createDApp(body) {
    const response = await axios({
        method: "POST",
        url: `${CORE_SERVICE_URL}/dapps`,
        headers: {
            "Content-Type": "application/json",
            Authorization: getToken(),
        },
        data: JSON.stringify(body),
        timeout: 30000,
    });
    return response;
}

export async function updateDApp(dappId, body) {
    const response = await axios({
        method: "PUT",
        url: `${CORE_SERVICE_URL}/dapps/${dappId}`,
        headers: {
            "Content-Type": "application/json",
            Authorization: getToken(),
        },
        data: JSON.stringify(body),
        timeout: 30000,
    }).catch((error) => {
        return { data: { status: 400, error: error.response.statusText } };
    });
    return response.data;
}

export async function deleteDApps(dappId) {
    const response = await axios({
        method: "DELETE",
        url: `${CORE_SERVICE_URL}/dapps/${dappId}`,
        headers: {
            "Content-Type": "application/json",
            Authorization: getToken(),
        },
        timeout: 30000,
    }).catch((error) => {
        return { data: { status: 400, error: error.response.statusText } };
    });
    return response.data;
}

export async function getDetailDAppById(dappId) {
    const response = await axios({
        method: "GET",
        url: `${CORE_SERVICE_URL}/dapps/${dappId}`,
        headers: {
            "Content-Type": "application/json",
            Authorization: getToken(),
        },
        timeout: 30000,
    }).catch((error) => {
        return { data: { status: 400, error: error.response.statusText } };
    });
    return response.data;
}

export async function retryCreateDapp(dappId) {
    const response = await axios({
        method: "POST",
        url: `${CORE_SERVICE_URL}/dapps/${dappId}/retry`,
        headers: {
            "Content-Type": "application/json",
            Authorization: getToken(),
        },
        timeout: 30000,
    }).catch((error) => {
        return { data: { status: 400, error: error.response.statusText } };
    });
    return response.data;
}
export async function retryUpdateDapp(dappId) {
    const response = await axios({
        method: "PUT",
        url: `${CORE_SERVICE_URL}/dapps/${dappId}/retry`,
        headers: {
            "Content-Type": "application/json",
            Authorization: getToken(),
        },
        timeout: 30000,
    }).catch((error) => {
        return { data: { status: 400, error: error.response.statusText } };
    });
    return response.data;
}
export async function rollBackDapp(dappId) {
    const response = await axios({
        method: "PUT",
        url: `${CORE_SERVICE_URL}/dapps/${dappId}/rollback`,
        headers: {
            "Content-Type": "application/json",
            Authorization: getToken(),
        },
        timeout: 30000,
    }).catch((error) => {
        return { data: { status: 400, error: error.response.statusText } };
    });
    return response.data;
}
export async function retryDeleteDapp(dappId) {
    const response = await axios({
        method: "DELETE",
        url: `${CORE_SERVICE_URL}/dapps/${dappId}/retry`,
        headers: {
            "Content-Type": "application/json",
            Authorization: getToken(),
        },
        timeout: 30000,
    }).catch((error) => {
        return { data: { status: 400, error: error.response.statusText } };
    });
    return response.data;
}
