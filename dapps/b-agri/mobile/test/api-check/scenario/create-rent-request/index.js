const fs = require("fs");

// get user role;
module.exports = async function(iRequest, configs, headers, funcName) {
   
    const wstream = fs.createWriteStream(funcName + "/result-test.json");

    console.time(funcName);
    // project Id cần chính xác với customerId ! 

    const response = await iRequest(configs.APP_API + "/msx-lead/api/domain/v1/customer/service-request", "POST", headers, {}, null, {
        "projectId": "dac78bae-ae59-4808-9c63-c68a2ec55c5d", //  dự án New Star
        // "projectId": "62625a33-98fa-4f3d-9d56-b99141ebbf92",
        
        "repoType": "rent", // require
        "title": "Cho thuê", // require
        "description": "-", // require 
       
        "customData": {
            "contractId": null,
            "rentData": {
                "propertyId": "A1-01-04",  // mã sản phẩm
                "price": "2000022", // số tiền |  giá
                "unit": "vnđ", // đơn vị vnd | usd
                "type": "tháng", // loại cho thuê theo tháng / năm
                "period": "1", // thời gian thuê
                "deposit": "1", // đặt cọc
                "note": "note", // ghi chú
                "province": "Hàn Nội", // tỉnh thành phố
                "district": "Hoàng Mai", // quận huyện
                "ward": "Gốc Đề", //  phường
                "address": "11 Võ Văn Ngân",
                "images": [
                    "https://dxs-o2o-static.s3-ap-southeast-1.amazonaws.com/1632797182343_Screenshot_20210923_185926.png"
                ],
                "files": [
                ],
                "customerCode": "KH-000000071" // user login không cần sửa
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

