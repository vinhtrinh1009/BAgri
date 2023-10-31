
const fs = require("fs");

// create main menu at home page;
module.exports = async function(iRequest, configs, headers, funcName) {

    const wstream = fs.createWriteStream("./result-test/scenario/" + funcName + "on");

    console.time(funcName);

    let response = await iRequest(configs.APP_API + "/msx-care/api/domain/v1/customer/resident/updateFamily", "PUT", headers, {}, null, {
        
        "id": "0582674e-976c-4137-9407-933b8ece3e8d", // id apartment
        "familyId": "ece752a0-d884-4999-a846-3930957d9fbc", // id thanh vien 
        "family": {
            "name": "AAAA", 
            "code": null,
            "gender": null,
            "birthdayYear": "09/06/2021", // require this format
            "contactAddress": "",
            "bornAddress": "",
            "rootAddress": "",
            "email": null,
            "phone": null,
            "identityId": null,
            "identityValue": null,
            "identityIssuedDate": null,
            "identityIssuedPlace": "",
            "job": "",
            "nation": "",
            "religion": "",
            "relationship": "",
            "status": "active"
        }
    });

    console.log(response);

    console.timeEnd(funcName);

    const message = JSON.stringify(response, null, "\t");
    
    // finish write;
    wstream.write(message);
    wstream.end(function () {
        console.log("check", funcName, "done\n");
    });
};
