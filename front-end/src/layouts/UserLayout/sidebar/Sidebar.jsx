import React, { useEffect, useState } from "react";
import { Grid } from "react-feather";
import { menu } from "../menu";
import { Link } from "react-router-dom";
import { useLocation } from "react-router";
import { imagePath } from "../../../constant/imagePath";

export default function Sidebar() {
    const location = useLocation();
    const [activeUrl, setActiveUrl] = useState(location.pathname);
    useEffect(() => {
        setActiveUrl(location.pathname);
    }, [location]);
    return (
        <>
            <div className="vchain_sidebar">
                <div className="vchain_logo_wrapper">
                    <img className="vchain_logo logo_light_theme" src={imagePath.LOGO_LIGHT} alt="" height="41.26" width="152.89" />
                    <img className="vchain_logo logo_dark_theme" src={imagePath.LOGO_DARK} alt="" height="41.26" width="152.89" />
                    <img className="vchain_logo logo_short" src={imagePath.LOGO_SHORT} alt="" height="41.26" width="41.26" />
                    <label htmlFor="check_toggle_sidebar" className="toggle_sidebar">
                        <Grid width={16} height={16} />
                    </label>
                </div>
                <ul className="vchain_menu mt-4">
                    {menu.map((item, index) => {
                        return (
                            <li key={"menu" + item.title + index}>
                                <Link to={item.url}>
                                    <div className={`vchain_menu_item ${activeUrl.includes(item.url) ? "active_router" : ""}`}>
                                        <span className="item_icon">{item.icon}</span>
                                        <span className="item_title">{item.title}</span>
                                    </div>
                                </Link>
                                <ul>
                                    {item.childs.map((child, i) => {
                                        return (
                                            <li key={"menu" + child.title + i}>
                                                <Link to={child.url}>
                                                    <div className={`vchain_menu_item submenu ${activeUrl === child.url ? "active_router" : ""}`}>
                                                        <span className="item_icon"></span>
                                                        <span className="item_title">{child.title}</span>
                                                    </div>
                                                </Link>
                                            </li>
                                        );
                                    })}
                                </ul>
                            </li>
                        );
                    })}
                </ul>
            </div>
            <label htmlFor="check_toggle_sidebar" className="toggle_sidebar_bg"></label>
        </>
    );
}
