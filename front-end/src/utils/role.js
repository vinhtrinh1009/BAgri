import { getRemember } from "./token";

const ROLE = {
    USER: "user",
    GUEST: "guest"
}

function setLocalRole(role) {
    localStorage.setItem("role", role);
}

function setSessionRole(role) {
    sessionStorage.setItem("role", role);
}

function setRole(role) {
    if (getRemember()) {
        localStorage.setItem("role", role);
    } else {
        sessionStorage.setItem("role", role);
    }
}

function getRole() {
    const remember = getRemember();
    return remember ? localStorage.getItem("role") : sessionStorage.getItem("role");
}

function clearRole() {
    const remember = getRemember();
    return remember ? localStorage.removeItem("role") : sessionStorage.removeItem("role");
}

function getRouteByRole(role) {
    if (role === ROLE.USER) {
        return "/dapps";
    } else if (role === ROLE.GUEST) {
        return "/login"
    }
}

export { ROLE, getRouteByRole, setLocalRole, setSessionRole, getRole, clearRole, setRole };
