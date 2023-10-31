const { default: jwtDecode } = require("jwt-decode");
const { getToken } = require("./mng-token");

function isEnable2FA() {
  const token = getToken();
  const jwtToken = token.split(" ")[1];
  const decodedToken = jwtDecode(jwtToken);
  return decodedToken.twoFAVerified;
}

export { isEnable2FA };
