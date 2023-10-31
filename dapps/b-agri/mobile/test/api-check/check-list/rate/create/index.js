
const fs = require("fs");

// get user role;
module.exports = async function(iRequest, configs, headers, funcName) {

    const wstream = fs.createWriteStream(funcName + "/result-test.json");

    console.time(funcName);
    const response = await iRequest(configs.APP_API + "/msx-rating/api/domain/v1/rating", "POST", headers, {}, null, {
        forLeadCare: {
            "id": "77fd8dad-a7c7-46fb-809c-35a75ae767a9-1"
        },
        ratingBy: {
            "name": "Mãi Thị Huy",
            "id": "77fd8dad-a7c7-46fb-809c-35a75ae767a9"
        },
        ratingByIp: "",
        value: 3,
        description: ""
    });
    console.timeEnd(funcName);

    const message = JSON.stringify(response, null, "\t");

    // finish write;
    wstream.write(message);
    wstream.end(function () {
        console.log("check", funcName, "done\n");
    });
};
