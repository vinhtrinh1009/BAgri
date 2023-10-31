const uriRegister  = require("./uri-register.js");
const uriRequest  = require("./uri-request.js");
const fs = require("fs");
const BASE_API = "https://apistaging.realagent.vn";


function registerAll(dir, callback) {
    var files = fs.readdirSync(dir);
    for (var i in files) {
        var name = dir + '/' + files[i];
        if (fs.statSync(name).isDirectory()){
            registerAll(name, callback);
        } else if ((/\.js$/i).test(files[i])) {
            callback(dir, name);
        }
    }
}

(async function() {
    
    if (!fs.existsSync("./result-test")) {
        fs.mkdirSync("./result-test");
    }

    registerAll("./check-list", (dir, file) => {
        uriRegister.addFunc(dir, require(file));
    });

    const configs = {
        APP_API: BASE_API
    };

    const headers = {
        "content-type": "application/json",
    };

    // user login first to get token;
    try {
        const response = await uriRequest(BASE_API + "/msx-sts/api/domain/v1/auth/mobile/login", "POST", headers, {}, null, {
            "email": "",
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
