import React from "react";
import { useEffect } from "react";
import { useLocation } from "react-router";
import AlertCustom from "./alert/AlertCustom";
import Content from "./content/Content";
import Header from "./header/Header";
import Sidebar from "./sidebar/Sidebar";

export default function UserLayout() {
    const location = useLocation();
    useEffect(() => {
        if (!localStorage.getItem("token")) {
            localStorage.clear();
            sessionStorage.clear();
            window.location.href = "/login";
        }
    }, [location]);
    return (
        <div className="vchain_layout">
            <input type="checkbox" id="check_toggle_sidebar" style={{ display: "none" }} />
            <div className="vchain_content_swapper">
                <Header />
                <Content />
            </div>
            <Sidebar />
            <AlertCustom />
        </div>
    );
}
