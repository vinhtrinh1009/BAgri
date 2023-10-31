import { useEffect, useState } from "react";
import React from "react";
import Avatar from "@mui/material/Avatar";
import { Col, Row } from "reactstrap";
import "../index.scss";
import { Button, MenuItem } from "@material-ui/core";
import TextField from "@mui/material/TextField";
import { useDispatch, useSelector } from "react-redux";
import { UPDATE_PROFILE } from "src/redux/User/Settings/actionTypes";
import { useNavigate } from "react-router";
import { OPEN_WARNING_ALERT } from "src/redux/User/Alerts/actionTypes";
import { Edit } from "@material-ui/icons";

export default function Account() {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const user = useSelector((state) => state.User.user);
    const [profile, setProfile] = useState();
    const [icon, setIcon] = useState("none");

    const locals = [
        {
            value: "HaNoi",
            label: "HN",
        },
        {
            value: "HoChiMinh",
            label: "TPHCM",
        },
        {
            value: "DaNang",
            label: "DN",
        },
        {
            value: "HaiPhong",
            label: "HP",
        },
    ];

    const handleEditProfile = () => {
        setProfile(null);
        dispatch({ type: UPDATE_PROFILE, payload: { user_id: user.user_id, data: profile } });
        dispatch({
            type: OPEN_WARNING_ALERT,
            payload: {
                message: "Request is being processed",
            },
        });
    };
    const handleDisableAcc = () => {
        setProfile({ active: false });
        dispatch({ type: UPDATE_PROFILE, payload: { user_id: user.user_id, data: { active: false } } });
    };

    function uploadImg(e) {
        const file = e.target.files[0];
        let reader = new FileReader();
        reader.onload = function (ee) {
            dispatch({ type: UPDATE_PROFILE, payload: { user_id: user.user_id, data: { ...profile, avatar: ee.target.result } } });
        };
        if (file) {
            reader.readAsDataURL(file);
        }
        dispatch({
            type: OPEN_WARNING_ALERT,
            payload: {
                message: "Request is being processed",
            },
        });
    }

    return (
        <Row style={{ padding: "30px" }}>
            <Col lg={4} style={{ display: "flex", justifyContent: "center", alignItems: "center" }}>
                <div style={{ display: "inline-block", width: "150px", height: "150px", overflow: "hidden", position: "relative" }}>
                    <Avatar alt="" src={`${user?.avatar}` || "src/assets/images/dashboard/profile.jpg"} style={{ width: "inherit", height: "inherit" }} />
                    <span className="icon-badge" style={{ position: "absolute", right: "16px", bottom: "5px" }}>
                        <Edit fontSize="small" />
                    </span>
                    <input
                        style={{ position: "absolute", top: 0, left: 0, display: "block", width: "inherit", height: "inherit", borderRadius: "50%", cursor: "pointer", opacity: "0" }}
                        onChange={uploadImg}
                        type="file"
                        id="drop_zone"
                    />
                </div>
            </Col>
            <Col lg={8} style={{ paddingBottom: "30px" }}>
                <Row style={{ marginBottom: "20px" }}>
                    <Col style={{ fontSize: "25px", fontWeight: "bold" }}>{user?.full_name}</Col>
                    <Col style={{ display: "flex", justifyContent: "right" }}>
                        <Button
                            variant="outlined"
                            color="secondary"
                            className="btn-disable"
                            onClick={() => {
                                if (window.confirm("Are you want to disable this account?") === true) {
                                    handleDisableAcc();
                                }
                            }}
                        >
                            Disable account
                        </Button>
                    </Col>
                </Row>
                <Row>
                    <Col md={6} style={{ marginBottom: "20px" }}>
                        <TextField size="small" label="Full Name" variant="filled" fullWidth onChange={(e) => setProfile({ ...profile, full_name: e.target.value })} />
                    </Col>
                    <Col md={6} style={{ marginBottom: "20px" }}>
                        <TextField select size="small" label="Local" variant="filled" fullWidth onChange={(e) => setProfile({ ...profile, location: e.target.value })}>
                            {locals.map((option) => (
                                <MenuItem key={option.value} value={option.value}>
                                    {option.label}
                                </MenuItem>
                            ))}
                        </TextField>
                    </Col>
                    <Col md={6} style={{ marginBottom: "20px" }}>
                        <TextField type="tel" size="small" label="Phone" variant="filled" fullWidth onChange={(e) => setProfile({ ...profile, phone: e.target.value })} />
                    </Col>
                    <Col md={6} style={{ marginBottom: "20px" }}>
                        <TextField size="small" label="Birthday" variant="filled" fullWidth onChange={(e) => setProfile({ ...profile, birthday: e.target.value })} />
                    </Col>
                    <Col>
                        <Button variant="contained" color="primary" className="btn-editProfile" onClick={() => handleEditProfile()}>
                            Edit profile
                        </Button>
                    </Col>
                </Row>
            </Col>
        </Row>
    );
}
