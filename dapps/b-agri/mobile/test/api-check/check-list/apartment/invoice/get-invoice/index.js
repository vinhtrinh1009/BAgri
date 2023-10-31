
const fs = require("fs");

// get user role;
module.exports = async function(iRequest, configs, headers, funcName) {

    const wstream = fs.createWriteStream(funcName + "/result-test.json");

    console.time(funcName);
    const response = await iRequest(configs.APP_API + "/msx-utility/api/query/v1/customer/invoice/c35af28c-7384-453a-8091-4a3acc079a82", "GET", headers, {}, null, {});
    console.timeEnd(funcName);

    const message = JSON.stringify(response, null, "\t");

    // finish write;
    wstream.write(message);
    wstream.end(function () {
        console.log("check", funcName, "done\n");
    });
};
