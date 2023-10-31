
const fs = require("fs");

// get user role;
module.exports = async function(iRequest, configs, headers, funcName) {

    const wstream = fs.createWriteStream("./result-test/admin/" + funcName + "on");

    console.time(funcName);
    const response = await iRequest(configs.APP_API + "/msx-master-data/api/v1/master/app-config", "POST", headers, {}, null, {
        "appName": "DxBQL", 
        "screenName": "Home", 
        "functionName": "display",
        "type": "icon",
        "value":"data:image/png;base64,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"
    });
    console.timeEnd(funcName);

    const message = JSON.stringify(response, null, "\t");

    // finish write;
    wstream.write(message);
    wstream.end(function () {
        console.log("check", funcName, "done\n");
    });
};
