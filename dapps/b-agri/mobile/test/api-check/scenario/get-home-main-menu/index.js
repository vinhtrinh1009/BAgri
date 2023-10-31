
const fs = require("fs");

// create main menu at home page;
module.exports = async function(iRequest, configs, headers, funcName) {

    const wstream = fs.createWriteStream("./scenario/" + funcName + "/result-test.json");

    console.time(funcName);

    
    const response = await iRequest(configs.APP_API + "/msx-master-data/api/v1/master/app-configs", "GET", headers, {}, null, {
        appName: "DxHome"
    });
    console.log(5, response);
    console.timeEnd(funcName);

    const message = JSON.stringify(response, null, "\t");
    
    // finish write;
    wstream.write(message);
    wstream.end(function () {
        console.log("check", funcName, "done\n");
    });
};
