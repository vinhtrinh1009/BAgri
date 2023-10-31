
const fs = require("fs");

// get user role;
module.exports = async function(iRequest, configs, headers, funcName) {

    const wstream = fs.createWriteStream(funcName + "/result-test.json");

    console.time(funcName);
    const response = await iRequest(configs.APP_API + "/msx-care/api/domain/v1/public/customer/isDuplicate", "POST", headers, {}, null, {
        email: "1234960@agamil.com",
        phone: "0913333960",
        identity: {
            "value": "013069060",
            "date": null, 
            "place": null
        }
    });
    console.timeEnd(funcName);

    const message = JSON.stringify(response, null, "\t");

    // finish write;
    wstream.write(message);
    wstream.end(function () {
        console.log("check", funcName, "done\n");
    });
};
