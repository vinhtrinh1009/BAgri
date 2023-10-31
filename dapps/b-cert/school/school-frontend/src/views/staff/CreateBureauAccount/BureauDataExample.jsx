import React from "react";
import DownloadExampleData from "../../../shared/DownloadExampleData";

export default function BureauDataExample() {
  const title = "Mẫu file dữ liệu Giáo vụ Viện";
  const fileName = "v1.2/giao-vu-example.xlsx";
  const head = ["Khoa/Viện*", "Bộ môn*", "Mã giáo vụ*", "Họ và tên*", "Email*", "Số điện thoại"];
  const body = [
    ["KCNTT", "CNPM", "GVu00001", "Bùi Thị Mai Anh", "anh.buithimai@hust.edu.vn", 976707772],
    ["KCNTT", "Innovation Centre", "GVu00002", "Nguyễn Thị Minh Châu", "chauntm@soict.hust.edu.vn"],
    ["KCNTT", "Innovation Centre", "GVu00003", "Michel Toulouse", "michel.toulouse@soict.hust.edu.vn"],
    ["KCNTT", "TTMT", "GVu00004", "Lại Tiến Đức", "duclt@soict.hust.edu.vn", 849300599],
    ["KCNTT", "TTMT", "GVu00005", "Phạm Thanh Liêm)", "liem.phamthanh@hust.edu.vn"],
    ["KCNTT", "TTMT", "GVu00006", "Trần Thị Dung", "dung.tranthi@hust.edu.vn", 985057800],
    // ["KCNTT", "CNPM", "GVu00007", "Lương Mạnh Bá", "balm@soict.hust.edu.vn", 915061199],
    // ["KCNTT", "KHMT", "GVu00008", "Ban Hà Bằng", "bang.banha@hust.edu.vn", 985819467],
    // ["KCNTT", "HTTT", "GVu00009", "Đỗ Bá Lâm", "lam.doba@hust.edu.vn", 964666475],
  ];
  return <DownloadExampleData {...{ title, fileName, head, body }}></DownloadExampleData>;
}
