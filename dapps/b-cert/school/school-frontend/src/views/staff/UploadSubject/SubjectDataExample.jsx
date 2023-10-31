import React from "react";
import DownloadExampleData from "../../../shared/DownloadExampleData";

export default function SubjectDataExample() {
  const title = "Mẫu file dữ liệu Môn học";
  const fileName = "v1.2/mon-hoc-example.xlsx";
  const head = ["Subject id", "name", "credits"];
  const body = [
    ["EM1170", "	Pháp luật đại cương", "2"],
    ["SSH1050", "Tư tưởng HCM	", "2"],
    ["IT1110", "Tin học đại cương", "3"],
    ["MI1110", "Giải tích I", "4"],
  ];
  return <DownloadExampleData {...{ title, fileName, head, body }}></DownloadExampleData>;
}
