import React, { useState } from "react";
import { Grid, LogIn, Moon, Sun, User } from "react-feather";
import { useDispatch, useSelector } from "react-redux";
import { clearToken } from "src/utils/token";
import { clearRole } from "src/utils/role";
import { clearUser } from "src/utils/user";
import { useNavigate } from "react-router-dom";
import { LAYOUT } from "src/redux/User/Storages/actionTypes";
import { useEffect } from "react";
import { userActions } from "src/redux/Guest/reducer";
import { imagePath } from "../../../constant/imagePath";

export default function Header() {
    const dispatch = useDispatch();
    useEffect(() => {
        dispatch(userActions.getProfile({ user_id: localStorage.getItem("user_id") }));
        if (localStorage.getItem("layout_version")) {
            document.body.className = localStorage.getItem("layout_version");
        } else {
            localStorage.setItem("layout_version", "light");
        }
    }, []);
    const user = useSelector((state) => state.User.user);
    const navigate = useNavigate();
    const [moonlight, setMoonlight] = useState(false);
    const MoonlightToggle = () => {
        if (localStorage.getItem("layout_version") == "dark-only") {
            dispatch({ type: LAYOUT, payload: "light" });
            setMoonlight("light");
            document.body.className = "light";
            localStorage.setItem("layout_version", "light");
        } else {
            dispatch({ type: LAYOUT, payload: "dark-only" });
            setMoonlight("dark-only");
            document.body.className = "dark-only";
            localStorage.setItem("layout_version", "dark-only");
        }
    };

    return (
        <div className="vchain_header">
            <div className="vchain_header_left">
                <img className="logo_header logo_light_theme" src={imagePath.LOGO_LIGHT} alt="" height="41.26" width="152.89" />
                <img className="logo_header logo_dark_theme" src={imagePath.LOGO_DARK} alt="" height="41.26" width="152.89" />
                <label htmlFor="check_toggle_sidebar" className="toggle_sidebar">
                    <Grid width={16} height={16} />
                </label>
            </div>
            <div className="vchain_header_right">
                <div className="mode" onClick={() => MoonlightToggle()}>
                    {localStorage.getItem("layout_version") == "dark-only" ? <Sun /> : <Moon />}
                </div>
                <div className="avata_wrapper">
                    <img
                        className="avata_img b-r-10"
                        style={{ objectFit: "cover" }}
                        width={40}
                        height={40}
                        src={user.avatar || "https://www.cyberlearning.ro/wp-content/uploads/learn-press-profile/5/591b6db105e1e6f3dfadecc9234d484a.jpg"}
                        alt=""
                    />
                    <div className="avata_title">
                        <b>{user.full_name || "No name"}</b>
                        <p className="mb-0 font-roboto">
                            {user.role == "user" ? "User" : "Admin"} <i className="middle fa fa-angle-down"></i>
                        </p>
                    </div>
                    <ul className="profile_dropdown">
                        <li className="dropdown_opt">
                            <User width={17} height={17} />
                            <span>{"Account"} </span>
                        </li>
                        <li
                            className="dropdown_opt"
                            onClick={(e) => {
                                clearToken();
                                clearRole();
                                clearUser();
                                navigate("/");
                            }}
                        >
                            <LogIn width={17} height={17} />
                            <span>{"LogOut"}</span>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    );
}
