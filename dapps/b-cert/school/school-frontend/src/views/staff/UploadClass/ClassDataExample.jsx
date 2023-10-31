import React from "react";
import DownloadExampleData from "../../../shared/DownloadExampleData";

export default function ClassDataExample() {
  const title = "Mẫu file dữ liệu Lớp học";
  const fileName = "v1.2/lop-hoc-example.xlsx";
  const head = ["Semester", "Class id", "Subject id", "Subject name", "Professor id", "Student list"];
  const body = [
    [
      20201,
      118161,
      "IT3180",
      "Nhập môn công nghệ phần mềm",
      "GV0001",
      "20195753,20195754,20195755,20195756,20196277,20196278,20195757,20195758,20195759",
    ],
    [
      20201,
      118585,
      "IT3040",
      "Kỹ thuật lập trình",
      "GV0001",
      "20195753,20195754,20195755,20195756,20196277,20196278,20195757,20195758,20195759",
    ],
    [
      20201,
      118614,
      "IT4501",
      "Đảm bảo chất lượng Phần mềm",
      "GV0001",
      "20195753,20195754,20195755,20195756,20196277,20196278,20195757,20195758,20195759",
    ],
    [
      20201,
      117873,
      "IT4501Q",
      "Đảm bảo chất lượng phần mềm ",
      "GV0001",
      "20195753,20195754,20195755,20195756,20196277,20196278,20195757,20195758,20195759",
    ],
    [
      20201,
      119435,
      "IT1140",
      "Tin học đại cương",
      "GV0003",
      "20195753,20195754,20195755,20195756,20196277,20196278,20195757,20195758,20195759",
    ],
    [
      20201,
      118626,
      "IT4906",
      "Tính toán tiến hóa",
      "GV0003",
      "20195753,20195754,20195755,20195756,20196277,20196278,20195757,20195758,20195759",
    ],
    [
      20201,
      121354,
      "IT3220",
      "C Programming (Introduction)",
      "GV0004",
      "20195753,20195754,20195755,20195756,20196277,20196278,20195757,20195758,20195759",
    ],
  ];
  return <DownloadExampleData {...{ title, fileName, head, body }}></DownloadExampleData>;
}
