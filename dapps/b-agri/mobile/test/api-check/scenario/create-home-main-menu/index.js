
const fs = require("fs");

// create main menu at home page;
module.exports = async function(iRequest, configs, headers, funcName) {

    const wstream = fs.createWriteStream("./result-test/scenario/" + funcName + "on");

    console.time(funcName);

    // encode image >> https://www.base64-image.de/
        
    // create main menu icon;
    // ic_menu_management_requests
    let respon = await iRequest(configs.APP_API + "/msx-master-data/api/v1/master/app-config", "POST", headers, {}, null, {
        "appName": "DxHome", 
        "screenName": "Home", 
        "functionName": "ManagementRequest",
        "section": "Main",
        "configuration": {
			"icon": "https://dxs-o2o-static.s3-ap-southeast-1.amazonaws.com/1632431315269_ic_menu_management_requests.png",
			"label": "Quản lý yêu cầu",
			"order": 1,
			"isActive": true,
			"accessible": true
		}
    });
    
    respon = await iRequest(configs.APP_API + "/msx-master-data/api/v1/master/app-config", "POST", headers, {}, null, {
        "appName": "DxHome", 
        "screenName": "Home", 
        "functionName": "NewsRealEstate",
        "section": "Main",
        "configuration": {
			"icon": "https://dxs-o2o-static.s3-ap-southeast-1.amazonaws.com/1632431402967_ic_menu_news_real_estate.png",
			"label": "Tin bất động sản",
			"order": 2,
			"isActive": true,
			"accessible": true
		}
    });
    
    respon = await iRequest(configs.APP_API + "/msx-master-data/api/v1/master/app-config", "POST", headers, {}, null, {
        "appName": "DxHome", 
        "screenName": "Home", 
        "functionName": "Promotion",
        "section": "Main",
        "configuration": {
			"icon": "https://dxs-o2o-static.s3-ap-southeast-1.amazonaws.com/1632430554357_ic_menu_endow.png",
			"label": "Ưu đãi",
			"order": 3,
			"isActive": true,
			"accessible": true
		}
    });
    
    respon = await iRequest(configs.APP_API + "/msx-master-data/api/v1/master/app-config", "POST", headers, {}, null, {
        "appName": "DxHome", 
        "screenName": "Home", 
        "functionName": "Utils",
        "section": "Main",
        "configuration": {
			"icon": "https://dxs-o2o-static.s3-ap-southeast-1.amazonaws.com/1632430554357_ic_menu_endow.png",
			"label": "Tiện ích",
			"order": 4,
			"isActive": true,
			"accessible": true
		}
    });

    respon = await iRequest(configs.APP_API + "/msx-master-data/api/v1/master/app-config", "POST", headers, {}, null, {
        "appName": "DxHome", 
        "screenName": "Home", 
        "functionName": "DeclarationOfMedical",
        "section": "Main",
        "configuration": {
			"icon": "https://dxs-o2o-static.s3-ap-southeast-1.amazonaws.com/1632430554357_ic_menu_endow.png",
			"label": "Khai báo y tế",
			"order": 5,
			"isActive": true,
			"accessible": true
		}
    });

    respon = await iRequest(configs.APP_API + "/msx-master-data/api/v1/master/app-config", "POST", headers, {}, null, {
        "appName": "DxHome", 
        "screenName": "Home", 
        "functionName": "CheckInWithQR",
        "section": "Main",
        "configuration": {
			"icon": "https://dxs-o2o-static.s3-ap-southeast-1.amazonaws.com/1632430554357_ic_menu_endow.png",
			"label": "Mã QR Check-In",
			"order": 6,
			"isActive": true,
			"accessible": true
		}
    });

    respon = await iRequest(configs.APP_API + "/msx-master-data/api/v1/master/app-config", "POST", headers, {}, null, {
        "appName": "DxHome", 
        "screenName": "Home", 
        "functionName": "ScanQR",
        "section": "Main",
        "configuration": {
			"icon": "https://dxs-o2o-static.s3-ap-southeast-1.amazonaws.com/1632430554357_ic_menu_endow.png",
			"label": "Quét Mã QR",
			"order": 7,
			"isActive": true,
			"accessible": true
		}
    });

    respon = await iRequest(configs.APP_API + "/msx-master-data/api/v1/master/app-config", "POST", headers, {}, null, {
        "appName": "DxHome", 
        "screenName": "Home", 
        "functionName": " AppointmentSchedule",
        "section": "Main",
        "configuration": {
			"icon": "https://dxs-o2o-static.s3-ap-southeast-1.amazonaws.com/1632430554357_ic_menu_endow.png",
			"label": "Đặt lịch hẹn",
			"order": 8,
			"isActive": true,
			"accessible": true
		}
    });


    console.log(4, respon);
    response = await iRequest(configs.APP_API + "/msx-master-data/api/v1/master/app-configs", "GET", headers, {}, null, {
        appName: "DxHome"
    });
    console.log(5, response);
    console.timeEnd(funcName);

    const message = JSON.stringify(response, null, "\t");
    
    // finish write;
    wstream.write(message);
    wstream.end(function () {
        console.log("check", funcName, "done\n");
    });
};
