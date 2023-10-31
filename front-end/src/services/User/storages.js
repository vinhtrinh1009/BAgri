import axios from "axios";
import { V_STORAGE_URL } from "src/constant/config";
import { getToken } from "src/utils/token";

export const storageApiUrl = {
    getUserFolder: `${V_STORAGE_URL}/folders`,
    createNewFolder: `${V_STORAGE_URL}/folders`,
    getRecents: `${V_STORAGE_URL}/recents`,
    getFavorites: `${V_STORAGE_URL}/favorites`,
    getTrash: `${V_STORAGE_URL}/trashes`,
    getShare: `${V_STORAGE_URL}/shares`,
    deleteAll: `${V_STORAGE_URL}/delete`,
    recoverAll: `${V_STORAGE_URL}/recovery`,
    getFolder: (idFolder) => {
        return `${V_STORAGE_URL}/folders/${idFolder}`;
    },
    getPlatformFolder: (idFolder) => {
        return `${V_STORAGE_URL}/shares/${idFolder}`;
    },
    markFavoriteFolder: (idFolder) => {
        return `${V_STORAGE_URL}/folders/${idFolder}/favorite`;
    },
    unfavoriteFolder: (idFolder) => {
        return `${V_STORAGE_URL}/folders/${idFolder}/unfavorite`;
    },
    uploadFolder: (idFolderContainer) => {
        return `${V_STORAGE_URL}/folders/${idFolderContainer}/upload`;
    },
    renameFolder: (idFolder) => {
        return `${V_STORAGE_URL}/folders/${idFolder}/rename`;
    },
    trashFolder: (idFolder) => {
        return `${V_STORAGE_URL}/folders/${idFolder}/trash`;
    },
    untrashFolder: (idFolder) => {
        return `${V_STORAGE_URL}/folders/${idFolder}/untrash`;
    },
    deleteFolder: (idFolder) => {
        return `${V_STORAGE_URL}/folders/${idFolder}/delete`;
    },
    moveFolder: (idFolder) => {
        return `${V_STORAGE_URL}/folders/${idFolder}/move`;
    },
    copyFolder: (idFolder) => {
        return `${V_STORAGE_URL}/folders/${idFolder}/copy`;
    },
    downloadFolder: (idFolder) => {
        return `${V_STORAGE_URL}/folders/${idFolder}/download`;
    },

    markFavoriteFile: (idFile) => {
        return `${V_STORAGE_URL}/files/${idFile}/favorite`;
    },
    unfavoriteFile: (idFile) => {
        return `${V_STORAGE_URL}/files/${idFile}/unfavorite`;
    },
    uploadFile: (idFolderContainer) => {
        return `${V_STORAGE_URL}/files/${idFolderContainer}/upload`;
    },
    trashFile: (idFile) => {
        return `${V_STORAGE_URL}/files/${idFile}/trash`;
    },
    untrashFile: (idFile) => {
        return `${V_STORAGE_URL}/files/${idFile}/untrash`;
    },
    deleteFile: (idFile) => {
        return `${V_STORAGE_URL}/files/${idFile}/delete`;
    },
    renameFile: (idFile) => {
        return `${V_STORAGE_URL}/files/${idFile}/rename`;
    },
    moveFile: (idFile) => {
        return `${V_STORAGE_URL}/files/${idFile}/move`;
    },
    copyFile: (idFile) => {
        return `${V_STORAGE_URL}/files/${idFile}/copy`;
    },
    downloadFile: (idFile) => {
        return `${V_STORAGE_URL}/files/${idFile}/download`;
    },
};

export const storageService = {
    getUserStorages: async function () {
        const response = await axios({
            method: "GET",
            url: storageApiUrl.getUserFolder,
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },
    getRecents: async function () {
        const response = await axios({
            method: "GET",
            url: storageApiUrl.getRecents,
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },
    getShare: async function () {
        const response = await axios({
            method: "GET",
            url: storageApiUrl.getShare,
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },
    getFavorites: async function () {
        const response = await axios({
            method: "GET",
            url: storageApiUrl.getFavorites,
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },
    getTrash: async function () {
        const response = await axios({
            method: "GET",
            url: storageApiUrl.getTrash,
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },
    createNewBlankFolder: async function (dataPost) {
        const response = await axios({
            method: "POST",
            url: storageApiUrl.createNewFolder,
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            data: dataPost,
            timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },
    renameFolder: async function (idFolder, dataPut) {
        const response = await axios({
            method: "PUT",
            url: storageApiUrl.renameFolder(idFolder),
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            data: dataPut,
            timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },
    moveFolder: async function (idFolder, dataPut) {
        const response = await axios({
            method: "PUT",
            url: storageApiUrl.moveFolder(idFolder),
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            data: dataPut,
            timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },
    copyFolder: async function (idFolder, dataPut) {
        const response = await axios({
            method: "PUT",
            url: storageApiUrl.copyFolder(idFolder),
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            data: dataPut,
            timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },
    downloadFolder: async function (idFolder) {
        const response = await axios({
            method: "GET",
            url: storageApiUrl.downloadFolder(idFolder),
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            responseType: "arraybuffer",
            // timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        // return {
        //     data: response,
        //     type: response.headers["content-type"],
        //     status: "success",
        // };
        return response;
    },
    deleteFolder: async function (idFolder) {
        const response = await axios({
            method: "DELETE",
            url: storageApiUrl.deleteFolder(idFolder),
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },
    trashFolder: async function (idFolder) {
        const response = await axios({
            method: "PUT",
            url: storageApiUrl.trashFolder(idFolder),
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },
    untrashFolder: async function (idFolder) {
        const response = await axios({
            method: "PUT",
            url: storageApiUrl.untrashFolder(idFolder),
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },
    getDataFolder: async function (idFolder) {
        const response = await axios({
            method: "GET",
            url: storageApiUrl.getFolder(idFolder),
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },
    getDataPlatformFolder: async function (idFolder) {
        const response = await axios({
            method: "GET",
            url: storageApiUrl.getPlatformFolder(idFolder),
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },
    markFavoriteFolder: async function (idFolder) {
        const response = await axios({
            method: "PUT",
            url: storageApiUrl.markFavoriteFolder(idFolder),
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },
    unfavoriteFolder: async function (idFolder) {
        const response = await axios({
            method: "PUT",
            url: storageApiUrl.unfavoriteFolder(idFolder),
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },
    uploadFolder: async function (idFolderContainer, formData) {
        const response = await axios({
            method: "POST",
            data: formData,
            url: storageApiUrl.uploadFolder(idFolderContainer),
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            // timeout: 300000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },

    markFavoriteFile: async function (idFile) {
        const response = await axios({
            method: "PUT",
            url: storageApiUrl.markFavoriteFile(idFile),
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },
    unfavoriteFile: async function (idFile) {
        const response = await axios({
            method: "PUT",
            url: storageApiUrl.unfavoriteFile(idFile),
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },
    uploadFile: async function (idFolderContainer, formData) {
        const response = await axios({
            method: "POST",
            data: formData,
            url: storageApiUrl.uploadFile(idFolderContainer),
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            // timeout: 300000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },
    renameFile: async function (idFile, dataPut) {
        const response = await axios({
            method: "PUT",
            url: storageApiUrl.renameFile(idFile),
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            data: dataPut,
            timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },
    moveFile: async function (idFile, dataPut) {
        const response = await axios({
            method: "PUT",
            url: storageApiUrl.moveFile(idFile),
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            data: dataPut,
            timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },
    copyFile: async function (idFile, dataPut) {
        const response = await axios({
            method: "PUT",
            url: storageApiUrl.copyFile(idFile),
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            data: dataPut,
            timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },
    downloadFile: async function (idFile) {
        const response = await axios({
            method: "GET",
            url: storageApiUrl.downloadFile(idFile),
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            responseType: "arraybuffer",
            // timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        // return {
        //     data: response,
        //     type: response.headers["content-type"],
        //     status: "success",
        // };
        return response;
    },
    deleteFile: async function (idFile) {
        const response = await axios({
            method: "DELETE",
            url: storageApiUrl.deleteFile(idFile),
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },
    trashFile: async function (idFile) {
        const response = await axios({
            method: "PUT",
            url: storageApiUrl.trashFile(idFile),
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },
    untrashFile: async function (idFile) {
        const response = await axios({
            method: "PUT",
            url: storageApiUrl.untrashFile(idFile),
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },

    deleteAll: async function () {
        const response = await axios({
            method: "DELETE",
            url: storageApiUrl.deleteAll,
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },
    recoverAll: async function () {
        const response = await axios({
            method: "PUT",
            url: storageApiUrl.recoverAll,
            headers: { "Content-Type": "application/json", Authorization: getToken() },
            timeout: 30000,
        }).catch((error) => {
            return { data: { status: 404, error: error } };
        });
        return response.data;
    },
};
