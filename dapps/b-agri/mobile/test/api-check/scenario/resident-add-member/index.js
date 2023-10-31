const fs = require("fs");

// get user role;
module.exports = async function(iRequest, configs, headers, funcName) {
   
    const wstream = fs.createWriteStream("./result-test/scenario/" + funcName + "/result-test.json");

    console.time(funcName);

    const response = await iRequest(configs.APP_API + "/msx-care/api/domain/v1/customer/resident/addFamily", "POST", headers, {}, null, {
        "id":"0582674e-976c-4137-9407-933b8ece3e8d", // customerId
        "family":{
            "name":"Tom Ngo",
            "code":"12346798",
            "gender":"male",
            "birthdayYear":"2017-10-21",
            "contactAddress":"ho hoho",
            "bornAddress":"hahah",
            "rootAddress":"fffff",
            "email":"tom@gmail.com",
            "phone":"12456789",
            "identityId":"45678123",
            "identityValue":"234343",
            "identityIssuedDate":"2012-10-21",
            "identityIssuedPlace":"ha noi",
            "job":"mau giao",
            "nation":"kinh",
            "religion":"khong",
            "relationship":"son",
            "status":"active"
        }
    });
    
    console.timeEnd(funcName);

    const message = JSON.stringify(response, null, "\t");

    // finish write;
    wstream.write(message);
    wstream.end(function () {
        console.log("check", funcName, "done\n");
    });
};

