import axios from "axios";
import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router";
import { ACCOUNT_SERVICE_URL } from "src/constant/config";
import { LOGOUT } from "src/redux/User/Settings/actionTypes";
import { getToken } from "src/utils/token";

export default function Verify() {
    const url = window.location.href;
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const user = useSelector((state) => state.User.user);
    const user_id = user.user_id;
    var content;
    if (url.indexOf("email") !== -1) {
        content = "email";
    } else if (url.indexOf("password") !== -1) {
        content = "password";
    }
    async function verify() {
        const response = await axios({
            method: "PUT",
            url: `${ACCOUNT_SERVICE_URL}/users/${user_id}/verify/${content}`,
            headers: {
                "Content-Type": "application/json",
                Authorization: getToken(),
            },
            timeout: 30000,
        }).then((res) => {
            if (res.data.status === "success") {
                if (content === "password") {
                    dispatch({ type: LOGOUT, payload: true });
                    localStorage.clear();
                    navigate("/login");
                } else {
                    navigate("/");
                }
            }
        });
        return response;
    }
    useEffect(() => {
        verify();
    }, []);
    return <div></div>;
}
