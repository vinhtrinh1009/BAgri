
const fs = require("fs");

// get user role;
module.exports = async function(iRequest, configs, headers, funcName) {

    const wstream = fs.createWriteStream(funcName + "/result-test.json");

    console.time(funcName);
    const response = await iRequest(configs.APP_API + "/msx-care/api/domain/v1/customer/updateProfile", "PUT", headers, {}, null, {
        "email": "1234960@agamil.com",
        "name": "123",
        "phone": "0913333960",
        "gender": "male",
        "address": "aaa-" + Date.now(),
        "dob": "2021-09-06",
        "identity": {
            "value": "013069060", 
            "date": "24/03/2021",
            "place":"Hà nội"
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
