const ROLE = {
  STAFF: "staff",
  BUREAU: "BUREAU",
  TEACHER: "professor",
  STUDENT: "student",
};

function setLocalRole(role) {
  localStorage.setItem("role", role);
}

function setSessionRole(role) {
  sessionStorage.setItem("role", role);
}

function getRole() {
  return sessionStorage.getItem("role") || localStorage.getItem("role");
}

function clearRole() {
  sessionStorage.removeItem("role");
  localStorage.removeItem("role");
}

export {ROLE, setLocalRole, setSessionRole, getRole, clearRole };
