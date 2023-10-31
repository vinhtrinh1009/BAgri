import { getRemember } from "./token";

function setLocalUser(user_id) {
    localStorage.setItem("user_id", user_id);

}

function setSessionUser(user_id) {
    sessionStorage.setItem("user_id", user_id);
}

function setUser(user_id) {
    if (getRemember()) {
        localStorage.setItem("user_id", user_id);
    } else {
        sessionStorage.setItem("user_id", user_id);
    }
}

function getUser() {
    const remember = getRemember();
    return remember ? localStorage.getItem("user_id") : sessionStorage.getItem("user_id");
}

function clearUser() {
    const remember = getRemember();
    return remember ? localStorage.removeItem("user_id") : sessionStorage.removeItem("user_id");
}

export { setLocalUser, setSessionUser, getUser, clearUser, setUser };
