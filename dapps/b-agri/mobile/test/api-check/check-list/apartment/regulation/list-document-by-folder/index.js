
const fs = require("fs");

// get user role;
module.exports = async function(iRequest, configs, headers, funcName) {

    const wstream = fs.createWriteStream(funcName + "/result-test.json");

    console.time(funcName);
    const response = await iRequest(configs.APP_API + "/msx-property/api/query/v1/customer/resident-document/findAllDocument?q=&page=1&pageSize=5&projectId=001fff8d-2876-aa1b-08f3-d98326351859&documentFolderId=02c11e6f-be85-4fdb-9df8-cf25e1d777a4", "GET", headers, {}, null, {});
    console.timeEnd(funcName);

    const message = JSON.stringify(response, null, "\t");

    // finish write;
    wstream.write(message);
    wstream.end(function () {
        console.log("check", funcName, "done\n");
    });
};
