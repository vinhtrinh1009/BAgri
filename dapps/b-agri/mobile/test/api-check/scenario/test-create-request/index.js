
const fs = require("fs");

// get user role;
module.exports = async function(iRequest, configs, headers, funcName) {
   
    const wstream = fs.createWriteStream("./scenario/" + funcName + "/result-test.json");
    let message =  "";

    console.time(funcName);
    // request with photo;
    let response = await iRequest(configs.APP_API + "/msx-lead/api/domain/v1/public/service-request", "POST", headers, {}, null, {
        "title": "DxHome",
        "description": "jsjssj",
        "repoType": "project",
        "projectId": "f62c6135-0103-46ef-8907-87ba086b420d",
        "name": "nin",
        "email": "a@b.com",
        "phone": "0987987987",
        "customData": {
            "images": null,
            "contractId": null,
            "unitCode": null,
            "price": null,
            "transferPrice": null,
            "commission": null,
            "code": null,
            "address": null,
            "projectData": {
            "requestType": null,
            "name": null,
            "value": "jsjssj",
            "type": "text",
            "images": null,
            "files": null,
            "customerCode": null
            }
        },
        "customerId": null,
        "repoQuestion": null
    });

    response = await iRequest(configs.APP_API + "/msx-lead/api/domain/v1/customer/service-request", "POST", headers, {}, null, {
        "title": "DxHome",
        "description": "ko",
        "repoType": "project",
        "projectId": "f62c6135-0103-46ef-8907-87ba086b420d",
        "name": "123",
        "email": "1234960@agamil.com",
        "phone": "0913333960",
        "customData": {
            "images": null,
            "contractId": null,
            "unitCode": null,
            "price": null,
            "transferPrice": null,
            "commission": null,
            "code": null,
            "address": null,
            "projectData": {
            "requestType": "Yêu cầu tư vấn dự án",
            "name": "Có hài lòng",
            "value": "ko",
            "type": "text",
            "images": null,
            "files": null,
            "customerCode": "KH-000000071"
            }
        },
        "customerId": "77fd8dad-a7c7-46fb-809c-35a75ae767a9",
        "repoQuestion": "Có hài lòng"
    });

    console.timeEnd(funcName);
    
    message += JSON.stringify(response, null, "\t");

    // finish write;
    wstream.write(message);
    wstream.end(function () {
        console.log("check", funcName, "done\n");
    });
};

