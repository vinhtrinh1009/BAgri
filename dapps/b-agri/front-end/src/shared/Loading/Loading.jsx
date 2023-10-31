import React from "react";
import { ImagePath } from "../../constants/ImagePath";
import "./loading.scss";
export default function Loading() {
    return (
        <div className="season" style={{ position: "fixed", top: "0", left: "0", width: "100vw", height: "100vh", zIndex: "100", background: "#fff" }}>
            <img src={ImagePath.LOGO} alt="" />
            <div className="loading loader">
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
            </div>
            <img src={ImagePath.BG} className="bg" alt="" />
        </div>
    );
}
