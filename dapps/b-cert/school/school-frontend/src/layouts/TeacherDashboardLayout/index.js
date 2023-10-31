import { makeStyles } from "@material-ui/core";
import axios from "axios";
import React, { useEffect, useState } from "react";
import PerfectScrollbar from "react-perfect-scrollbar";
import { useDispatch, useSelector } from "react-redux";
import { Outlet } from "react-router-dom";
import Loading from "src/shared/Loading";
import { setProfile } from "src/views/teacher/Profile/redux";
import NavBar from "./NavBar";
import TopBar from "./TopBar";
import { getUser } from "src/utils/mng_user";
import { useSnackbar } from "notistack";
import { ERR_TOP_CENTER } from "../../utils/snackbar-utils";

const useStyles = makeStyles((theme) => ({
    root: {
        height: "100%",
        width: "100%",
        display: "flex",
        overflow: "hidden",
        backgroundColor: theme.palette.background.dark,
    },
    wrapper: {
        flex: "1 1 auto",
        display: "flex",
        overflow: "hidden",
        paddingTop: 64,
        [theme.breakpoints.up("lg")]: {
            paddingLeft: 256,
        },
    },
    contentContainer: {
        flex: "1 1 auto",
        display: "flex",
        overflow: "hidden",
    },
    content: {
        flex: "1 1 auto",
        // height: "100%",
        overflow: "auto",
    },
}));

const TeacherDashboardLayout = () => {
    const classes = useStyles();
    const [isMobileNavOpen, setMobileNavOpen] = useState(false);
    const loading = useSelector((state) => state.teacherProfileSlice.fetching);
    const { enqueueSnackbar, closeSnackbar } = useSnackbar();
    const dp = useDispatch();
    const user = getUser();

    useEffect(() => {
        fetchProfile();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    async function fetchProfile() {
        try {
            const response = await axios.get("/professor/" + user + "/");
            dp(setProfile(response.data));
        } catch (error) {
            enqueueSnackbar("Phiên làm việc đã kết thúc, vui lòng đăng nhập lại!", ERR_TOP_CENTER);
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

export default TeacherDashboardLayout;
