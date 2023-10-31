import { ERR_TOP_CENTER, INFO_TOP_CENTER } from "./snackbar-utils";
import { getUser } from "./mng_user";
import axios from "axios"
import { User } from "react-feather";

let privateKeyHex = null;

export function setPrivateKeyHex(privateKeyHexParam) {
  privateKeyHex = privateKeyHexParam;
}

// export function getPrivateKeyHex() {
//   return privateKeyHex;
// }

export async function requirePrivateKeyHex(user) {
    if (privateKeyHex) return privateKeyHex;
//   enqueueSnackbar("Hãy mở ví và chọn tài khoản!", INFO_TOP_CENTER);
//   return new Promise((resolve, reject) => {
//     const tabId = Math.floor(Math.random() * 9999);
//     window.addEventListener("message", function (event) {
//       if (event.data.type === "SIGN_RESPONSE" && event.data.tabId === tabId) {
//         if (event.data.accept) {
//           privateKeyHex = event.data.account.privateKey;
//           resolve(privateKeyHex);
//         } else {
//           enqueueSnackbar("Bạn cần chọn một tài khoản để có thể thực hiện thao tác này!", ERR_TOP_CENTER);
//           reject();
//         }
//       }
//     });
//     window.postMessage({ type: "SIGN_REQUEST", tabId });
//   });
    
    privateKeyHex = await axios.get("/api/v1/get-private-key/?user="+user)
}
