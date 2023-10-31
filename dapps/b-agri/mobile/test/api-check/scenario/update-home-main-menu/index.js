
const fs = require("fs");

// create main menu at home page;
module.exports = async function(iRequest, configs, headers, funcName) {

    const wstream = fs.createWriteStream("./result-test/scenario/" + funcName + "on");

    console.time(funcName);

    // encode image >> https://www.base64-image.de/
        
    // create main menu icon;
    // ic_menu_management_requests
    // await iRequest(configs.APP_API + "/msx-master-data/api/v1/master/app-config/a7d2278a-194e-437a-bda1-80c0e17979d1", "PUT", headers, {}, null, {
    //     "appName": "DxHome", 
    //     "screenName": "Home", 
    //     "functionName": "ManagementRequest",
    //     "section": "Main",
    //     "configuration": {
	// 		"icon": "https://dxs-o2o-static.s3-ap-southeast-1.amazonaws.com/1632431315269_ic_menu_management_requests.png",
	// 		"label": "Quản lý yêu cầu",
	// 		"order": 1,
	// 		"isActive": true,
	// 		"accessible": true
	// 	}
    // });

    // await iRequest(configs.APP_API + "/msx-master-data/api/v1/master/app-config/9f35dc6e-2a69-4730-8084-5bef6b843e05", "PUT", headers, {}, null, {
    //     "appName": "DxHome", 
    //     "screenName": "Home", 
    //     "functionName": "ManagementRequest",
    //     "section": "Main",
    //     "configuration": {
	// 		"icon": "https://dxs-o2o-static.s3-ap-southeast-1.amazonaws.com/1632431402967_ic_menu_news_real_estate.png",
	// 		"label": "Tin bất động sản",
	// 		"order": 3,
	// 		"isActive": true,
	// 		"accessible": true
	// 	}
    // });

    // await iRequest(configs.APP_API + "/msx-master-data/api/v1/master/app-config/3fe14673-ea92-4129-bf3e-445b315a3ae1", "PUT", headers, {}, null, {
    //     "appName": "DxHome", 
    //     "screenName": "Home", 
    //     "functionName": "ManagementRequest",
    //     "section": "Main",
    //     "configuration": {
	// 		"icon": "https://dxs-o2o-static.s3-ap-southeast-1.amazonaws.com/1632430554357_ic_menu_endow.png",
	// 		"label": "Ưu đãi",
	// 		"order": 4,
	// 		"isActive": true,
	// 		"accessible": true
	// 	}
    // });

    let response = await iRequest(configs.APP_API + "/msx-master-data/api/v1/master/app-config/3cf61650-8e0e-4952-b038-331ae9d37930", "PUT", headers, {}, null, {
        "appName": "DxHome", 
        "screenName": "Home", 
        "functionName": "ManagementRequest",
        "section": "Main",
        "configuration": {
			"icon": "https://dxs-o2o-static.s3-ap-southeast-1.amazonaws.com/1632431315269_ic_menu_management_requests.png",
			"label": "Là gì vậy",
			"order": 4,
			"isActive": true,
			"accessible": true
		}
    });
 
    // response = await iRequest(configs.APP_API + "/msx-master-data/api/v1/master/app-configs", "GET", headers, {}, null, {
    //     appName: "DxHome"
    // });
    console.log(response);
    console.timeEnd(funcName);

    const message = JSON.stringify(response, null, "\t");
    
    // finish write;
    wstream.write(message);
    wstream.end(function () {
        console.log("check", funcName, "done\n");
    });
};
