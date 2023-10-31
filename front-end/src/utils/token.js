import axios from "axios";

let remember = true;

function setRemember(_remember) {
    remember = _remember;
}

function getRemember() {
    return remember;
}

function setToken(token) {
    if (remember) localStorage.setItem("token", token);
    else sessionStorage.setItem("token", token);
}

function setSessionToken(token) {
    axios.defaults.headers.common["Authorization"] = token;
    sessionStorage.setItem("token", token);
}

function setLocalToken(token) {
    axios.defaults.headers.common["Authorization"] = token;
    localStorage.setItem("token", token);
}

function getToken() {
    const remember = getRemember();
    return remember ? "Bearer " + localStorage.getItem("token") : "Bearer " + sessionStorage.getItem("token");
}

function getBareToken() {
    const remember = getRemember();
    return remember ? localStorage.getItem("token") : sessionStorage.getItem("token");
}

function clearToken() {
    if (remember) {
        axios.defaults.headers.common["Authorization"] = null;
        localStorage.removeItem("token");
        localStorage.removeItem('user');
        localStorage.removeItem('display')
    } else {
        sessionStorage.removeItem("token");
    }
}

export { setSessionToken, setLocalToken, getToken, getBareToken, clearToken, setRemember, getRemember, setToken };
