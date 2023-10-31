import React from "react";
import { Outlet } from "react-router";

export default function Content() {
    return (
        <div className="vchain_content">
            <Outlet />
        </div>
    );
}
