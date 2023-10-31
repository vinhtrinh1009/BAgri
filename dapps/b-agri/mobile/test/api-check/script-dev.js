const uriRegister  = require("./uri-register.js");
const uriRequest  = require("./uri-request.js");
const fs = require("fs");
const BASE_API = "http://localhost:68";

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
    
    const configs = {
        APP_API: BASE_API
    };

    const headers = {
        "content-type": "application/json",
    };

    // user login first to get token;
    try {
        const response = await uriRequest(BASE_API + "/msx-sts/api/domain/v1/auth/login", "POST", headers, {}, null, {
            "email": "0913333960",
            "password": "",
            "system":"care",
            "authType": "local", 
            "deviceToken": ""
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
