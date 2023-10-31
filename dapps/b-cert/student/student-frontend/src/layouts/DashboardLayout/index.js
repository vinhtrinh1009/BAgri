import React, { useEffect, useState } from "react";
import { Outlet } from "react-router-dom";
import { makeStyles } from "@material-ui/core";
import NavBar from "./NavBar";
import TopBar from "./TopBar";
import { getToken } from "../../utils/mng-token";
import { setProfile } from "../../views/StudentProfile/redux";
import { useDispatch, useSelector } from "react-redux";
import Loading from "../../shared/Loading";
import PerfectScrollbar from "react-perfect-scrollbar";
import axios from "axios";
import { useSnackbar } from "notistack";
import { ERR_TOP_CENTER } from "../../utils/snackbar-utils";

const useStyles = makeStyles((theme) => ({
    root: {
        backgroundColor: theme.palette.background.dark,
        display: "flex",
        height: "100%",
        overflow: "hidden",
        width: "100%",
    },
    wrapper: {
        display: "flex",
        flex: "1 1 auto",
        overflow: "hidden",
        paddingTop: 64,
        [theme.breakpoints.up("lg")]: {
            paddingLeft: 256,
        },
    },
    contentContainer: {
        display: "flex",
        flex: "1 1 auto",
        overflow: "hidden",
    },
    content: {
        flex: "1 1 auto",
        height: "100%",
        overflow: "auto",
    },
}));

const DashboardLayout = () => {
    const classes = useStyles();
    const [isMobileNavOpen, setMobileNavOpen] = useState(false);
    const loading = useSelector((state) => state.studentProfileSlice.fetching);
    const userid = localStorage.getItem("user");
    const { enqueueSnackbar } = useSnackbar();
    const dp = useDispatch();

    useEffect(() => {
        fetchStudentProfile();
    }, []);

    async function fetchStudentProfile() {
        try {
            const response = await axios.get("/student/" + userid + "/");
            dp(setProfile(await response.data));
        } catch (err) {
            console.log(err);
            enqueueSnackbar("Token expired", ERR_TOP_CENTER);
            localStorage.clear();
            sessionStorage.clear();
            setTimeout(() => {
                window.location.href = "/dang-nhap";
            }, 1000);
        }
    }

    return (
        <>
            {loading ? (
                <Loading />
            ) : (
                <>
                    <div className={classes.root}>
                        <TopBar onMobileNavOpen={() => setMobileNavOpen(true)} />
                        <NavBar onMobileClose={() => setMobileNavOpen(false)} openMobile={isMobileNavOpen} />
                        <div className={classes.wrapper}>
                            <div className={classes.contentContainer}>
                                <div className={classes.content}>
                                    <PerfectScrollbar>
                                        <Outlet />
                                    </PerfectScrollbar>
                                </div>
                            </div>
                        </div>
                    </div>
                </>
            )}
        </>
    );
};

export default DashboardLayout;
