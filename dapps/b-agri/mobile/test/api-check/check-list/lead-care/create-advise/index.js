
const fs = require("fs");

// get user role;
module.exports = async function(iRequest, configs, headers, funcName) {

    const wstream = fs.createWriteStream(funcName + "/result-test.json");

    console.time(funcName);
    // request with photo;
    const response = await iRequest(configs.APP_API + "/msx-lead/api/domain/v1/lead/pub", "POST", headers, {}, null, {
        "type": "PRIMARY",
        "name": "Pham Hai Long",
        "email": "emailgmail.com",
        "phone": "0123456778", 
        "description": "Yeu cau tu van",
        "address": "" 
    });
    console.timeEnd(funcName);

    const message = JSON.stringify(response, null, "\t");

    // finish write;
    wstream.write(message);
    wstream.end(function () {
        console.log("check", funcName, "done\n");
    });
};

