import React, { Fragment } from "react";
import { Outlet } from "react-router-dom";
import AlertCustom from "../UserLayout/alert/AlertCustom";
// import Loader from "src/shared/Loading";
// import PerfectScrollbar from "react-perfect-scrollbar";

const GuestLayout = () => {
    return (
        <Fragment>
            {/* <Loader /> */}
            <Outlet />
            <AlertCustom />
        </Fragment>
    );
};

export default GuestLayout;
