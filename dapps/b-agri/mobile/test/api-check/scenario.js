const uriRegister  = require("./uri-register.js");
const uriRequest  = require("./uri-request.js");
const fs = require("fs");
const BASE_API = "https://apistaging.realagent.vn";

// sample command:
// node scenario.js create-rent-request dev
(async function() {

    if (!fs.existsSync("./scenario")) {
        fs.mkdirSync("./scenario");
    }

    if (process.argv[2]) {
        const file = process.argv[2];
        if (fs.existsSync("./scenario/" + file + "/index.js")) {
            uriRegister.addFunc(file, require("./scenario/" + file + "/index.js"));
        }
    } else {
        console.log("\n \u001b[31mscenario source is require like this:\n \u001b[33m$ node scenario.js create-home-main-menu", "\u001b[0m\n");
    }
    
    const isDevEnv = process.argv[3] && process.argv[3].toString().toLocaleLowerCase() === "dev";
    const BASE_API = isDevEnv ? "http://localhost:68" : "https://apistaging.realagent.vn";
    const account = isDevEnv ? "0913333960" : "0915915915";
    const password = isDevEnv ? "12345678" : "Abc12345";

    const configs = {
        APP_API: BASE_API
    };

    const headers = {
        "content-type": "application/json",
    };
    console.log("configs", configs);
    // user login first to get token;
    try {
        const response = await uriRequest(BASE_API + "/msx-sts/api/domain/v1/auth/login", "POST", headers, {}, null, {
            "password": password,
            "email": account,
            "system":"care",
            "authType": "local", 
            "deviceToken": "e23kqcuYRFa2XdnKgzSDCp:APA91bH5_WC0iBojQ_M3ZR8ihCY8nHT5Me"
        });
        console.log("token", response);
        headers["Authorization"] = `Bearer ${response.access_token}`;
    } catch(e) {

    }

    uriRegister.getAllFunc().forEach(funcName => {
        const func = uriRegister.getFuncByName(funcName);
       
        if (func) {
            try {
                func(uriRequest, configs, headers, funcName);
            } catch(e) {
                console.log("error", funcName);
            }
        }
    });
})();
