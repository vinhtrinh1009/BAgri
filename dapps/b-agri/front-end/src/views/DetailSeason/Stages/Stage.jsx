import React, { useState } from "react";
import { ExpandMore } from "@mui/icons-material";
import Lightbox from "react-image-lightbox";
import "react-image-lightbox/style.css";
import { diffTime, fDate } from "../../../utils/formatTime";

export default function Stage(props) {
    const { title = "", steps = [], indexStage = "", allTasks = [] } = props;
    function getTask(stepName) {
        return allTasks.filter((task, index) => task.stage_name == title && task.step_name == stepName);
    }
    return (
        <>
            <div className="stage_title">{title}</div>
            <div className="stage_content">
                {steps.map((step, index) => {
                    return <Step dataStep={step} key={"step" + indexStage + "_" + index} tasks={getTask(step.name)} id={"step" + indexStage + "_" + index} />;
                })}
            </div>
        </>
    );
}

function Step(props) {
    const { dataStep = {}, tasks = [], id = "" } = props;
    const [expaned, setExpaned] = useState(false);

    return (
        <>
            <label className="step_woking" onClick={() => setExpaned(!expaned)}>
                <span className="icon_circle"></span>
                <span className="step_title">{dataStep.name}</span>
                <span className="icon_arrow" style={{ transformOrigin: "center", transform: expaned ? "rotateX(180deg)" : "rotateX(0deg)", transition: "0.3s" }}>
                    <ExpandMore width={14} height={14} />
                </span>
            </label>
            <div className="step_content" style={{ height: expaned ? `${237 * tasks.length + 40}px` : "0" }}>
                {tasks.map((task, index) => {
                    return <Task key={"task" + id + index} taskData={task} />;
                })}
            </div>
        </>
    );
}

function Task(props) {
    const { taskData } = props;
    const [imgLightBox, setImgLightBox] = useState({ isOpen: false, photoIndex: 0 });
    const images = taskData.result.result;
    function getFarmer() {
        if (taskData.farmer?.farmers) {
            return taskData.farmer.farmers.join(", ");
        }
        return "";
    }
    return (
        <>
            <div className="step_content_card">
                <div className="data_row">
                    <span className="data_row_title">Công việc</span>
                    <span className="data_row_content">{taskData.name}</span>
                </div>
                <div className="data_row">
                    <span className="data_row_title">Thời gian</span>
                    <span className="data_row_content">{diffTime(taskData.end_time, taskData.start_time)}</span>
                </div>
                <div className="data_row">
                    <span className="data_row_title">Bắt đầu</span>
                    <span className="data_row_content">{fDate(taskData.start_time)}</span>
                </div>
                <div className="data_row">
                    <span className="data_row_title">Kết thúc</span>
                    <span className="data_row_content">{fDate(taskData.end_time)}</span>
                </div>
                <div className="data_row">
                    <span className="data_row_title">Nông dân</span>
                    <span className="data_row_content">{getFarmer()}</span>
                </div>
                <div className="data_row">
                    <span className="data_row_title">Công cụ</span>
                    <span className="data_row_content">{taskData.items}</span>
                </div>
                <div className="data_row" style={{ color: "rgba(119, 184, 30, 1)" }}>
                    <span className="data_row_title" style={{ color: "rgba(119, 184, 30, 1)" }}>
                        Kết quả
                    </span>
                    <span className="data_row_content" style={{ cursor: "pointer" }}>
                        <span onClick={() => setImgLightBox({ isOpen: true, photoIndex: 0 })} style={{ color: "rgba(119, 184, 30, 1)", marginRight: "5px", textDecoration: "underline" }}>
                            Xem chi tiết
                        </span>
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="14"
                            height="14"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            className="feather feather-external-link"
                        >
                            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
                            <polyline points="15 3 21 3 21 9" />
                            <line x1="10" y1="14" x2="21" y2="3" />
                        </svg>
                    </span>
                </div>
            </div>
            <div className="data_row">
                    <span className="data_row_title">Txid</span>
                    <span className="data_row_content">
                    {/* https://testnet.bscscan.com/tx/${taskData.txid */}
                        <a href={`https://explorer.v-chain.vn/explorer/6260fc7b7588d56cb67d07aa/transactions/${taskData.txid}`} target="_blank" style={{ color: "rgba(0, 0, 0, 1)", marginRight: "5px" }}>
                            {taskData.txid.slice(0,20) + "..."}
                        </a>
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="14"
                            height="14"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            className="feather feather-external-link"
                        >
                            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
                            <polyline points="15 3 21 3 21 9" />
                            <line x1="10" y1="14" x2="21" y2="3" />
                        </svg>
                    </span>
                </div>
            {imgLightBox.isOpen && (
                <Lightbox
                    mainSrc={images[imgLightBox.photoIndex]}
                    nextSrc={images[(imgLightBox.photoIndex + 1) % images.length]}
                    prevSrc={images[(imgLightBox.photoIndex + images.length - 1) % images.length]}
                    mainSrcThumbnail={images[imgLightBox.photoIndex]}
                    nextSrcThumbnail={images[(imgLightBox.photoIndex + 1) % images.length]}
                    prevSrcThumbnail={images[(imgLightBox.photoIndex + images.length - 1) % images.length]}
                    onCloseRequest={() =>
                        setImgLightBox((prev) => {
                            return { ...prev, isOpen: false };
                        })
                    }
                    onMovePrevRequest={() =>
                        setImgLightBox((prev) => {
                            return {
                                ...prev,
                                photoIndex: (prev.photoIndex + images.length - 1) % images.length,
                            };
                        })
                    }
                    onMoveNextRequest={() =>
                        setImgLightBox((prev) => {
                            return {
                                ...prev,
                                photoIndex: (prev.photoIndex + 1) % images.length,
                            };
                        })
                    }
                />
            )}
        </>
    );
}
