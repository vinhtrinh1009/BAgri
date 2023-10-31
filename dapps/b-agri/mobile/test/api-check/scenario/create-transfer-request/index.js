const fs = require("fs");

// get user role;
module.exports = async function(iRequest, configs, headers, funcName) {

    const wstream = fs.createWriteStream(funcName + "/result-test.json");

    console.time(funcName);
    // project Id cần chính xác với customerId ! 
    
    const response = await iRequest(configs.APP_API + "/msx-lead/api/domain/v1/customer/service-request", "POST", headers, {}, null, {
        "projectId": "f62c6135-0103-46ef-8907-87ba086b420d", //  dự án VINHOMES OCEAN PARK
        
        "repoType": "transfer", // require
        "title": "Yêu cầu đăng ký chuyển nhượng", // require
        "description": "Tôi 77fd8dad-a7c7-46fb-809c-35a75ae767a9 muốn đăng ký chuyển nhượng A1-12-03 của VINHOMES OCEAN PARK", // require 
       
        "customData": {
            "transferData": {
                "contractId": "12c4f114-2409-4ca4-a0e2-62c8113b9242", // mã hợp đồng
                "unitCode":"A1-12-03", // mã sản phầm giống propertyId
                "price":"2400000000", // giá hợp đồng
                "transferPrice":"123", // giá chuyển nhượng
                "commission":"10", // phí hoa hồng
                "code":"HĐC-VOP01-00020", // mã hợp đồng
                "province": "Bắc Giang", // tỉnh thành phố
                "district": "H. Việt Yên", // quận huyện
                "ward": "X. Vân Trung", //  phường
                // "address":"666, X. Vân Trung, H. Việt Yên, Bắc Giang"
                "address":"666", // địa chỉ
                "images": [
                    "https://dxs-o2o-static.s3-ap-southeast-1.amazonaws.com/1632797182343_Screenshot_20210923_185926.png"
                ],
                "customerCode": "KH-000000071", // user login không cần 
            },
        },

        "name": "123", // user login không cần sửa 
        "email": "1234960@agamil.com", // user login không cần sửa
        "phone": "0913333960", // user login không cần sửa
        "customerId": "77fd8dad-a7c7-46fb-809c-35a75ae767a9", // user login không cần sửa
    });
    
    console.timeEnd(funcName);

    const message = JSON.stringify(response, null, "\t");

    // finish write;
    wstream.write(message);
    wstream.end(function () {
        console.log("check", funcName, "done\n");
    });
};

