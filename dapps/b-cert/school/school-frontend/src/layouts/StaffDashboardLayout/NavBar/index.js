import { Avatar, Box, Divider, Drawer, Hidden, List, makeStyles, Typography } from "@material-ui/core";
import AccountBalanceIcon from "@material-ui/icons/AccountBalance";
import AspectRatioIcon from "@material-ui/icons/AspectRatio";
import CancelPresentationIcon from "@material-ui/icons/CancelPresentation";
import GroupAddIcon from "@material-ui/icons/GroupAdd";
import HowToVoteIcon from "@material-ui/icons/HowToVote";
import { Link2 } from "react-feather";
import PersonAddIcon from "@material-ui/icons/PersonAdd";
import SupervisorAccountIcon from "@material-ui/icons/SupervisorAccount";
import PropTypes from "prop-types";
import React, { useEffect } from "react";
import { useSelector } from "react-redux";
import { Link as RouterLink, useLocation } from "react-router-dom";
import ClassroomIcon from "../../../assets/icons/ClassroomIcon";
import NavItem from "./NavItem";

const items = [
    {
        href: "/cb-pdt/dang-ki-tham-gia",
        icon: AccountBalanceIcon,
        title: "Đăng kí tham gia",
    },
    //   {
    //     href: "/cb-pdt/bo-phieu",
    //     icon: HowToVoteIcon,
    //     title: "Bỏ phiếu",
    //   },
    // {
    //   href: "/cb-pdt/tao-tk-giao-vu",
    //   icon: PersonAddIcon,
    //   title: "Tạo tài khoản giáo vụ",
    // },
    {
        href: "/cb-pdt/tao-tk-giang-vien",
        icon: PersonAddIcon,
        title: "Tạo tài khoản giảng viên",
    },
    {
        href: "/cb-pdt/tao-tk-sinh-vien",
        icon: GroupAddIcon,
        title: "Tạo tài khoản sinh viên",
    },
    {
        href: "/cb-pdt/upload-mon-hoc",
        icon: ClassroomIcon,
        title: "Upload môn học",
    },
    {
        href: "/cb-pdt/upload-lop-hoc",
        icon: ClassroomIcon,
        title: "Upload lớp học",
    },
    {
        href: "/cb-pdt/upload-bang-cap",
        icon: AspectRatioIcon,
        title: "Upload bằng cấp",
    },
    {
        href: "/cb-pdt/thu-hoi-bang-cap",
        icon: CancelPresentationIcon,
        title: "Thu hồi bằng câp",
    },
    {
        href: "/cb-pdt/giao-dich-blockchain",
        icon: Link2,
        title: "Giao dịch blockchain",
    },
];

const useStyles = makeStyles(() => ({
    mobileDrawer: {
        width: 256,
    },
    desktopDrawer: {
        width: 256,
        top: 64,
        height: "calc(100% - 64px)",
    },
    avatar: {
        cursor: "pointer",
        width: 64,
        height: 64,
    },
}));

const NavBar = ({ onMobileClose, openMobile }) => {
    const classes = useStyles();
    const location = useLocation();

    const user = useSelector((state) => state.profileSlice);

    useEffect(() => {
        if (openMobile && onMobileClose) {
            onMobileClose();
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [location.pathname]);

    const content = (
        <Box height="100%" display="flex" flexDirection="column">
            <Box alignItems="center" display="flex" flexDirection="column" p={2}>
                <Avatar className={classes.avatar} component={RouterLink} src={user.imgSrc} to="/cb-pdt/dang-ki-tham-gia" />
                <Typography className={classes.name} color="textPrimary" variant="h5">
                    {user.university_name || "Trường ĐH ABC"}
                </Typography>
                <Typography color="textSecondary" variant="body2">
                    {"Cán bộ Trường"}
                </Typography>
            </Box>
            <Divider />
            <Box p={2}>
                <List>
                    {items.map((item) => (
                        <NavItem href={item.href} key={item.title} title={item.title} icon={item.icon} />
                    ))}
                </List>
            </Box>
            <Box flexGrow={1} />
        </Box>
    );

    return (
        <>
            <Hidden lgUp>
                <Drawer anchor="left" classes={{ paper: classes.mobileDrawer }} onClose={onMobileClose} open={openMobile} variant="temporary">
                    {content}
                </Drawer>
            </Hidden>
            <Hidden mdDown>
                <Drawer anchor="left" classes={{ paper: classes.desktopDrawer }} open variant="persistent">
                    {content}
                </Drawer>
            </Hidden>
        </>
    );
};

NavBar.propTypes = {
    onMobileClose: PropTypes.func,
    openMobile: PropTypes.bool,
};

NavBar.defaultProps = {
    onMobileClose: () => {},
    openMobile: false,
};

export default NavBar;
