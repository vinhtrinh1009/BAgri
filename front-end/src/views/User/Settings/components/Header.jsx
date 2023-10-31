import { Button } from "@material-ui/core";
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { CATEGORY } from "src/redux/User/Settings/actionTypes";
import "../index.scss";

export default function HeaderSetting() {
    const dispatch = useDispatch();
    const category = useSelector((state) => state.Setting.category);
    const handleCategory = (value) => {
        dispatch({ type: CATEGORY, payload: value });
    };
    return (
        <div className="headerSetting">
            {/* <Button variant="text" className={category === "notification" ? `active` : `btn-header`} onClick={() => handleCategory("notification")}>
                Notification
            </Button> */}
            <Button variant="text" className={category === "account" ? `active` : `btn-header`} onClick={() => handleCategory("account")}>
                Account
            </Button>
            <Button variant="text" className={category === "password" ? `active` : `btn-header`} onClick={() => handleCategory("password")}>
                Password
            </Button>
            <Button variant="text" className={category === "email" ? `active` : `btn-header`} onClick={() => handleCategory("email")}>
                Email
            </Button>

            {/* <Button variant="text" className={category === "plan" ? `active` : `btn-header`} onClick={() => handleCategory("plan")}>
                Plan
            </Button> */}
        </div>
    );
}
