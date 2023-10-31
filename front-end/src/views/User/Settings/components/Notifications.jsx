import React, { useState } from "react";
import Grid from "@mui/material/Grid";
import { Checkbox, Button } from "@material-ui/core";
import "../index.scss";
import { useDispatch, useSelector } from "react-redux";
import { UPDATE_PROFILE } from "src/redux/User/Settings/actionTypes";
import { OPEN_SUCCESS_ALERT } from "src/redux/User/Alerts/actionTypes";

export default function Notifications() {
    const dispatch = useDispatch();
    const user = useSelector((state) => state.User.user);
    const [notification, setNotification] = useState(user.notification);
    const user_id = user.user_id;
    const handleSubmit = () => {
        const data = { notification: notification };
        dispatch({ type: UPDATE_PROFILE, payload: { user_id: user_id, data: data } });
        dispatch({
            type: OPEN_SUCCESS_ALERT,
            payload: {
                message: "Successful!",
            },
        });
    };
    return (
        <Grid container spacing={2} style={{ display: "flex", justifyContent: "center", marginTop: "48px", marginBottom: "100px" }}>
            <Grid container md={4} xs={4}>
                <Grid item md={4} xs={4}></Grid>
                <Grid container md={6} xs={6}>
                    <Grid item md={6} xs={6} className="noti-title">
                        {"On UI"}
                    </Grid>
                    <Grid item md={6} xs={6} className="noti-title">
                        {"To Email"}
                    </Grid>
                </Grid>
                <br />
                <Grid item md={4} xs={4} className="noti-action">
                    {"Network activity"}
                </Grid>
                <Grid container md={6} xs={6}>
                    <Grid item md={6} xs={6} className="d-center">
                        <Checkbox
                            checked={notification.network.UI}
                            onChange={(e, checked) => setNotification({ ...notification, network: { ...notification.network, UI: checked } })}
                            style={{ color: "#1998F4" }}
                        ></Checkbox>
                    </Grid>
                    <Grid item md={6} xs={6} className="d-center">
                        <Checkbox
                            checked={notification.network.Email}
                            onChange={(e, checked) => setNotification({ ...notification, network: { ...notification.network, Email: checked } })}
                            style={{ color: "#1998F4" }}
                        ></Checkbox>
                    </Grid>
                </Grid>
                <br />
                <Grid item md={4} xs={4} className="noti-action">
                    {"DApp activity"}
                </Grid>
                <Grid container md={6} xs={6}>
                    <Grid item md={6} xs={6} className="d-center">
                        <Checkbox
                            checked={notification.dapp.UI}
                            onChange={(e, checked) => setNotification({ ...notification, dapp: { ...notification.dapp, UI: checked } })}
                            style={{ color: "#1998F4" }}
                        ></Checkbox>
                    </Grid>
                    <Grid item md={6} xs={6} className="d-center">
                        <Checkbox
                            checked={notification.dapp.Email}
                            onChange={(e, checked) => setNotification({ ...notification, dapp: { ...notification.dapp, Email: checked } })}
                            style={{ color: "#1998F4" }}
                        ></Checkbox>
                    </Grid>
                </Grid>
                <br />
                <Grid item md={4} xs={4} className="noti-action">
                    {"Token activity"}
                </Grid>
                <Grid container md={6} xs={6}>
                    <Grid item md={6} xs={6} className="d-center">
                        <Checkbox
                            checked={notification.token.UI}
                            onChange={(e, checked) => setNotification({ ...notification, token: { ...notification.token, UI: checked } })}
                            style={{ color: "#1998F4" }}
                        ></Checkbox>
                    </Grid>
                    <Grid item md={6} xs={6} className="d-center">
                        <Checkbox
                            checked={notification.token.Email}
                            onChange={(e, checked) => setNotification({ ...notification, token: { ...notification.token, Email: checked } })}
                            style={{ color: "#1998F4" }}
                        ></Checkbox>
                    </Grid>
                </Grid>
                <Grid md={12} xs={12} style={{ textAlign: "right", marginRight: "20%", marginTop: "5%" }}>
                    <Button variant="contained" color="primary" onClick={() => handleSubmit()}>
                        Submit
                    </Button>
                </Grid>
            </Grid>
        </Grid>
    );
}
