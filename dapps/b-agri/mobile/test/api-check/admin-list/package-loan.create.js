const fs = require("fs");

// get user role;
module.exports = async function(iRequest, configs, headers, funcName) {

    const wstream = fs.createWriteStream("./result-test/admin/" + funcName + "on");
    
    console.time(funcName);
    const response = await iRequest(configs.APP_API + "/msx-property/api/domain/v1/package-loan", "POST", headers, {}, null, {
        "name": "Gói vay lãi suất 6.9%",
        "bank": "Vietcombank 1",
        "projectId": "0b40923f-9546-4230-98d8-0355f3e00501",
        "interestRate": "6.9",
        "startDate": "Mon Sep 13 2021 00:50:34 GMT+0700 (Indochina Time)",
        "expirationDate": "Mon Sep 13 2022 00:50:34 GMT+0700 (Indochina Time)",
        "status": "ACTIVE",
        "description": "Ghi chú",
        "attachmentUrl": "https://portal.vietcombank.com.vn/Resources/no-image-news.jpg?RenditionID=3"
    });
    console.timeEnd(funcName);
   
    const message = JSON.stringify(response, null, "\t");
   
    // finish write;
    wstream.write(message);
    wstream.end(function () {
        console.log("check", funcName, "done\n");
    });
};