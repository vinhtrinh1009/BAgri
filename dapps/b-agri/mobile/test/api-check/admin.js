const uriRegister  = require("./uri-register.js");
const uriRequest  = require("./uri-request.js");
const fs = require("fs");
const BASE_API = "http://localhost:68";
// const BASE_API = "https://th-api.realagent.vn";

(async function() {
    
    if (!fs.existsSync("./result-test/admin")) {
        fs.mkdirSync("./result-test/admin");
    }

    if (!fs.existsSync("./admin-list")) {
        fs.mkdirSync("./admin-list");
    }

    if (process.argv[2]) {
        const file = process.argv[2];
        if (fs.existsSync("./admin-list/" + file)) {
            uriRegister.addFunc(file, require("./admin-list/" + file));
        }
    } else {
        const files = fs.readdirSync(__dirname + "/admin-list");
        // auto add script;
        files.forEach(file => {
            uriRegister.addFunc(file, require("./admin-list/" + file));
        });
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
            "email": "it.dxs@datxanh.com.vn",
            "password": "12345678",
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
