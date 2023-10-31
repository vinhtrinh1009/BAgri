import axios from "axios";
import { CORE_SERVICE_URL } from "src/constant/config";
import { getToken } from "src/utils/token";

export async function createNetwork(params) {
    const response = await axios({
        method: "POST",
        url: `${CORE_SERVICE_URL}/networks`,
        headers: {
            "Content-Type": "application/json",
            Authorization: getToken(),
        },
        data: params,
        timeout: 30000,
    }).catch((error) => {
        return { data: { status: 400, error: error.response.statusText } };
    });
    return response;
}

export async function retryCreateNetwork(idNetwork) {
    const response = await axios({
        method: "POST",
        url: `${CORE_SERVICE_URL}/networks/${idNetwork}/retry`,
        headers: {
            "Content-Type": "application/json",
            Authorization: getToken(),
        },
        timeout: 30000,
    }).catch((error) => {
        return { data: { status: 400, error: error.response.statusText } };
    });
    return response;
}

export async function getNetworkResources(idNetwork) {
    const response = await axios({
        method: "GET",
        url: `${CORE_SERVICE_URL}/networks/${idNetwork}/resources`,
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
export async function createNetworkResource(idNetwork, params) {
    const response = await axios({
        method: "POST",
        url: `${CORE_SERVICE_URL}/networks/${idNetwork}/resources`,
        headers: {
            "Content-Type": "application/json",
            Authorization: getToken(),
        },
        data: params,
        timeout: 30000,
    }).catch((error) => {
        return { data: { status: 400, error: error.response.statusText } };
    });
    return response.data;
}

export async function updateNetwork(idNetwork, params) {
    const response = await axios({
        method: "PUT",
        url: `${CORE_SERVICE_URL}/networks/${idNetwork}`,
        headers: {
            "Content-Type": "application/json",
            Authorization: getToken(),
        },
        data: params,
        timeout: 30000,
    }).catch((error) => {
        return { data: { status: 400, error: error.response.statusText } };
    });
    return response.data;
}

export async function retryUpdateNetwork(idNetwork) {
    const response = await axios({
        method: "PUT",
        url: `${CORE_SERVICE_URL}/networks/${idNetwork}/retry`,
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
export async function rollbackNetwork(idNetwork) {
    const response = await axios({
        method: "PUT",
        url: `${CORE_SERVICE_URL}/networks/${idNetwork}/rollback`,
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

export async function getNetwork(params) {
    const response = await axios({
        method: "GET",
        url: `${CORE_SERVICE_URL}/networks`,
        headers: {
            "Content-Type": "application/json",
            Authorization: getToken(),
        },
        timeout: 30000,
    });
    return response;
}

export async function deleteNetwork(idNetwork) {
    const response = await axios({
        method: "DELETE",
        url: `${CORE_SERVICE_URL}/networks/${idNetwork}`,
        headers: {
            "Content-Type": "application/json",
            Authorization: getToken(),
        },
        timeout: 30000,
    });
    return response;
}

export async function getNetworkById(idNetwork) {
    const response = await axios({
        method: "GET",
        url: `${CORE_SERVICE_URL}/networks/${idNetwork}`,
        headers: {
            "Content-Type": "application/json",
            Authorization: getToken(),
        },
        timeout: 30000,
    });
    return response;
}
