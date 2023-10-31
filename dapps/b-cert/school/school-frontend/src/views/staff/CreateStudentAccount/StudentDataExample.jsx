import React, { useEffect, useState } from "react";
import DownloadExampleData from "../../../shared/DownloadExampleData";
import axios from "axios";

export default function StudentDataExample() {
    const title = "Mẫu file dữ liệu Sinh viên";
    const fileName = "v1.2/sinh-vien-example.xlsx";
    const head = ["Student_id", "Last name", "First name", "Email", "Phone", "Address", "Unit", "Education_form"];
    const body = [
        ["20195753", "Do Hoa", "An", "an.dh295753@sis.hust.edu.vn", "125810987", "Hanoi", "KTMT-1125", "Cu nhan chinh quy"],
        ["20195754", "Hoang Dinh Luong", "An", "an.hdl195755@sis.hust.edu.vn", "125810988", "Ha Noi", "KHMT-1128", "Ki su chinh quy"],
        ["20195755", "Bui Hai", "Anh", "anh.bh955755@sis.hust.edu.vn", "125810989", "Ha Noi", "MMT-1124", "Cu nhan chinh quy"],
        ["20195756", "Bui Quang", "Anh", "anh.bq5756@sis.hust.edu.vn", "125810990", "Hai Phong", "KTMT-1125", "Cu nhan chinh quy"],
        ["20196277", "Đào Hoàng", "Anh", "anh.dh196277@sis.hust.edu.vn", "125810991", "Ha Noi", "KHMT-1128", "Ki su chinh quy"],
        ["20196278", "Đao Luong Duy", "Anh", "anh.dld296278@sis.hust.edu.vn", "125810992", "Nam Dinh", "MMT-1124", "Cu nhan chinh quy"],
    ];
    // const [body, setbody] = useState([]);
    // useEffect(() => {
    //     (async () => {
    //         const res = await axios.post(`http://dev.hust-edu.appspot.com/api/grades?accessKey=CJ2qNIdRNU7YuXQPTOGA-LamDB&classId=127001`);
    //         console.log(res.data);
    //         let data = "";
    //         setbody(
    //             res.data.data.map((item, index) => {
    //                 data = data + `${item.studentId}, `;
    //                 return [item.studentId, item.fullName, "", "", "", "", "", ""];
    //             })
    //         );
    //         console.log(data);
    //     })();
    // }, []);

    return <DownloadExampleData {...{ title, fileName, head, body }} minWidth={"2500px"}></DownloadExampleData>;
}
