
const fs = require("fs");

// get user role;
module.exports = async function(iRequest, configs, headers, funcName) {
   
    const wstream = fs.createWriteStream("./scenario/" + funcName + "/result-test.json");

    console.time(funcName);
    // request with photo;
    const response = await iRequest(configs.APP_API + "/msx-lead/api/domain/v1/customer/service-request", "POST", headers, {}, null, {

        "title": "Yêu cầu hoàn tất HĐ cọc", // require
        "description": "Tôi muốn hoàn tất HĐ cọc bởi hồ sơ bản cứng cho A1-01-02 của Central Park. Hãy hỗ trợ và cập nhật trạng thái giúp tôi.",
        "repoType": "project", // require
        "projectId": "1aa1eeed-f84d-424a-b2c6-e164a65c9366", // require
        "name": "Hien", // require
        "email": "hien@gmail.com", // require
        "phone": "0915915915", // require
        "customData": {
            "images": null,
            "contractId": "9f02e7f5-6143-4fe3-ba40-ecde81b80e50",
            "unitCode": null,
            "price": null,
            "transferPrice": null,
            "commission": null,
            "code": null,
            "address": null,
            "projectData": {
                "requestType": "Yêu cầu hoàn tất HĐ cọc",
                "type": "text",
                "value": "Tôi muốn hoàn tất HĐ cọc bởi hồ sơ bản cứng cho A1-01-02 của Central Park. Hãy hỗ trợ và cập nhật trạng thái giúp tôi.",
                "customerCode": "KH-000000185" // require
            },
        },
        "customerId": "7b4b94af-22a8-409d-a2fc-7cc227b931dd",
        "repoQuestion": null
    });
    
    console.timeEnd(funcName);

    console.log(response);

    const message = JSON.stringify(response, null, "\t");

    // finish write;
    wstream.write(message);
    wstream.end(function () {
        console.log("check", funcName, "done\n");
    });
};

