
const fs = require("fs");

// get user role;
module.exports = async function(iRequest, configs, headers, funcName) {
   
    const wstream = fs.createWriteStream("./scenario/" + funcName + "/result-test.json");

    console.time(funcName);
    // request with photo;
    const response = await iRequest(configs.APP_API + "/msx-lead/api/domain/v1/customer/service-request", "POST", headers, {}, null, {
        "title": "DxHome", // require
        "description": "--",
        "repoType": "project", // require
        "projectId": "db5a155a-083f-44ea-a36b-09e60b4e0d2b",
        "name": "Hien",
        "email": "hien@gmail.com", // user login data
        "phone": "0915915915", // user login data
        "customData": { // require
            "images": null,
            "contractId": null,
            "unitCode": null,
            "price": null,
            "transferPrice": null,
            "commission": null,
            "code": null,
            "address": null,
            "projectData": { // require
                "requestType": "Cấu hình dự án Royal",
                "name": "Khảo sát giá",
                "value": "aaa", // require
                "type": "text", // require
                "images": [
                    {"originalName":"image_picker597647801172077498.png","uploadName":"1635411042546_image_picker597647801172077498.png","url":"https://dxs-o2o-static.s3-ap-southeast-1.amazonaws.com/1635411042546_image_picker597647801172077498.png","fileType":"image"},
                    {"originalName":"image_picker5555988930420046075.png","uploadName":"1635410998122_image_picker5555988930420046075.png","url":"https://dxs-o2o-static.s3-ap-southeast-1.amazonaws.com/1635410998122_image_picker5555988930420046075.png","fileType":"image"}
                ],
                "files": [
                    {"originalName":"1-Postman.pdf","uploadName":"1635407249476_1_Postman.pdf","url":"https://dxs-o2o-static.s3-ap-southeast-1.amazonaws.com/1635407249476_1_Postman.pdf"}
                ],
                "customerCode": "KH-000000185" // require
            }
        },
        "customerId": "7b4b94af-22a8-409d-a2fc-7cc227b931dd", // user login data
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

