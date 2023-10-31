import React from "react";
import { Snackbar } from "@mui/material";
import MuiAlert from "@mui/material/Alert";
import { useDispatch } from "react-redux";
import { useSelector } from "react-redux";
import { CLOSE_ALERT } from "src/redux/User/Alerts/actionTypes";

export default function AlertCustom(props) {
    const dispatch = useDispatch();
    const { open = false, autoHideDuration = 4000, alertType = "info", message = "" } = useSelector((stores) => stores.Alert);
    const handleClose = (event, reason) => {
        if (reason === "clickaway") {
            return;
        }
        dispatch({ type: CLOSE_ALERT });
    };
    return (
        <Snackbar anchorOrigin={{ vertical: "top", horizontal: "center" }} open={open} autoHideDuration={autoHideDuration} onClose={handleClose} style={{ zIndex: "1000000", top: "90px" }}>
            <MuiAlert elevation={6} onClose={handleClose} severity={alertType} variant="filled">
                {message}
            </MuiAlert>
        </Snackbar>
    );
}
