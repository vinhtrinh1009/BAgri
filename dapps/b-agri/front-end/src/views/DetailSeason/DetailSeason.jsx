import React, { useEffect, useLayoutEffect, useState } from "react";
import { Typography } from "@mui/material";
import { ImagePath } from "../../constants/ImagePath";
import Stage from "./Stages/Stage";
import { useParams } from "react-router-dom";
import axios from "axios";
import Loading from "../../shared/Loading/Loading";

export default function DetailSeason() {
    const param = useParams();
    const [dataSeason, setDataSeason] = useState({ data: {}, loading: true });
    useLayoutEffect(() => {
        (async () => {
            try {
                const respone = await axios.get(`https://bagri.v-chain.vn/api/v1/seasons/network/${param.IdSeason}`);
                setTimeout(() => {
                    setDataSeason({ data: respone.data?.data?.season, loading: false });
                }, 1100);
                console.log(respone.data.data.season);
            } catch (e) {
                console.log(e);
                alert("Mã thông tin không đúng!");
                setDataSeason({ data: { error: true }, loading: false });
            }
        })();
    }, []);
    function handleNameSeason(name) {
        if (name) {
            return name.toLowerCase().replace("mùa vụ ", "");
        }
        return "";
    }
    function handleNameProcess(name) {
        if (name) {
            return name.toLowerCase().replace("quy trình", "");
        }
        return "";
    }
    return (
        <>
            {dataSeason.loading ? (
                <Loading />
            ) : (
                <>
                    {dataSeason.data.error ? (
                        <div className="season">
                            <img src={ImagePath.LOGO} alt="" />
                            <div className="error_data">
                                <div>404</div>
                                <div>Không tìm thấy!</div>
                            </div>
                            <img src={ImagePath.BG} className="bg" alt="" />
                        </div>
                    ) : (
                        <div className="season">
                            <img src={ImagePath.LOGO} alt="" />
                            <div className="title_box">
                                Mùa vụ <span style={{ color: "#77B81E" }}> {handleNameSeason(dataSeason.data?.name)} </span>
                            </div>
                            <div className="box_data">
                                <div className="data_row">
                                    <span className="data_row_title">ID mùa vụ</span>
                                    <span className="data_row_content">{dataSeason.data?.season_id}</span>
                                </div>
                                <div className="data_row">
                                    <span className="data_row_title">Trạng thái</span>
                                    <span className="data_row_content">{
                                        ("status" in dataSeason.data && dataSeason.data.status == "done") ? "Đã hoàn thành" : "Chưa hoàn thành"}</span>
                                </div>
                                <div className="data_row">
                                    <span className="data_row_title">Loại cây trồng</span>
                                    <span className="data_row_content">{dataSeason.data?.tree_name}</span>
                                </div>
                                <div className="data_row">
                                    <span className="data_row_title">Vườn</span>
                                    <span className="data_row_content">{dataSeason.data?.garden_name}</span>
                                </div>
                            </div>
                            <img src={ImagePath.BG} className="bg" alt="" />
                            <div className="title_box">
                                Quy trình <span style={{ color: "#77B81E" }}> {handleNameProcess(dataSeason.data?.process?.name)} </span>
                            </div>
                            {dataSeason.data?.process?.stages.map((stage, index) => {
                                return <Stage key={"stage" + stage.name + index} title={stage.name} steps={stage.steps} indexStage={index} allTasks={dataSeason.data.tasks} />;
                            })}
                        </div>
                    )}
                </>
            )}
        </>
    );
}
