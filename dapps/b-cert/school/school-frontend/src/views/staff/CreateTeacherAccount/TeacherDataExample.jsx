import React from "react";
import DownloadExampleData from "../../../shared/DownloadExampleData";

export default function TeacherDataExample() {
    const title = "Mẫu file dữ liệu Giảng viên";
    const fileName = "v1.2/giang-vien-example.xlsx";
    const head = ["department", "professor_id", "Last name", "First name", "Email", "Phone", "Address"];
    const body = [
        ["KCNTT", "GV00001", "Vu Van", "Thieu", "thieu.vuvan@hust.edu.vn", "982928307", ""],
        ["KCNTT", "GV00002", "Nguyen Phi", "Le", "le.nguyenphi@hust.edu.vn", "1662257624", ""],
        ["KCNTT", "GV00003", "Hirose", "Umi", "umi.hirose@soict.hust.edu.vn", "", ""],
        ["KCNTT", "GV00004", "Nguyen Ngoc", "Bich", "bichann@soict.hust.edu.vn", "1234567891", ""],
        ["KCNTT", "GV00005", "Ngo Lam", "Trung", "trung.ngolam@hust.edu.vn", "968395999", ""],
        ["KCNTT", "GV00006", "Do Ba", "Lam", "lam.doba@hust.edu.vn", "0945556768", ""],
        // ["KCNTT", "KHMT", "GV00007", "Nguyễn Linh Giang", "giang.nguyenlinh@hust.edu.vn", 912725672],
        // ["KCNTT", "HTTT", "GV00008", "Đỗ Quốc Huy", "huy.doquoc@hust.edu.vn", 936356172],
    ];
    return <DownloadExampleData {...{ title, fileName, head, body }} minWidth={"1500px"}></DownloadExampleData>;
}
