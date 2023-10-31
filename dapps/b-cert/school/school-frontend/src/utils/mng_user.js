import { getRemember } from "./mng-token";

function setLocalUser(user) {
  localStorage.setItem("user", user);
}

function setSessionUser(user) {
  sessionStorage.setItem("user", user);
}

function setLocalUniversity(university) {
    localStorage.setItem("university", university);
  }
  
  function setSessionUniversity(university) {
    sessionStorage.setItem("university", university);
  }

function setUser(user) {
  if (getRemember()) {
    localStorage.setItem("user", user);  
  } else {
    sessionStorage.setItem("user", user);
  }
}

function setUniversity(university){
    if (getRemember()) {
        localStorage.setItem("university", university);  
      } else {
        sessionStorage.setItem("university", university);
      }
}

function getUser() {
  const remember = getRemember();
  return remember ? localStorage.getItem("user") : sessionStorage.getItem("user");
}

function getUniversity() {
    const remember = getRemember();
    return remember ? localStorage.getItem("university") : sessionStorage.getItem("university");
  }

function clearUser() {
  const remember = getRemember();
  return remember ? localStorage.removeItem("user") : sessionStorage.removeItem("user");
}

function clearUniversity() {
    const remember = getRemember();
    return remember ? localStorage.removeItem("university") : sessionStorage.removeItem("university");
  }

export { setLocalUser, setSessionUser, getUser, clearUser, setUser, setLocalUniversity, setSessionUniversity, getUniversity, clearUniversity, setUniversity };
