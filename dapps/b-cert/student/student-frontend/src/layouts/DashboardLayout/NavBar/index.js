import React, { useEffect } from "react";
import { Link as RouterLink, useLocation } from "react-router-dom";
import PropTypes from "prop-types";
import { Avatar, Box, Divider, Drawer, Hidden, List, Typography, makeStyles } from "@material-ui/core";
import {
  AlertCircle as AlertCircleIcon,
  BarChart as BarChartIcon,
  Lock as LockIcon,
  Settings as SettingsIcon,
  ShoppingBag as ShoppingBagIcon,
  User as UserIcon,
  UserPlus as UserPlusIcon,
  Users as UsersIcon,
  Database as DatabaseIcon,
} from "react-feather";
import NavItem from "./NavItem";
import { useSelector } from "react-redux";

const user = {
  avatar: "/static/images/avatars/avatar_6.png",
  jobTitle: "Senior Developer",
  name: "Katarina Smith",
};

const items = [
  {
    href: "/student/thong-tin-ca-nhan",
    icon: UserIcon,
    title: "Thông tin cá nhân",
  },
  // {
  //   href: "/student/quan-ly-tai-khoan",
  //   icon: UsersIcon,
  //   title: "Quản lý tài khoản",
  // },
  {
    href: "/student/ket-qua-hoc-tap",
    icon: DatabaseIcon,
    title: "Kết quả học tập",
  },
  {
    href: "/student/chia-se-bang-cap",
    icon: ShoppingBagIcon,
    title: "Chia sẻ bằng cấp",
  },

  // {
  //   href: "/app/settings",
  //   icon: SettingsIcon,
  //   title: "Settings",
  // },
  // {
  //   href: "/login",
  //   icon: LockIcon,
  //   title: "Login",
  // },
  // {
  //   href: "/register",
  //   icon: UserPlusIcon,
  //   title: "Register",
  // },
  // {
  //   href: "/404",
  //   icon: AlertCircleIcon,
  //   title: "Error",
  // },
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

  const user = useSelector((state) => state.studentProfileSlice);

  useEffect(() => {
    if (openMobile && onMobileClose) {
      onMobileClose();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location.pathname]);

  const content = (
    <Box height="100%" display="flex" flexDirection="column">
      <Box alignItems="center" display="flex" flexDirection="column" p={2}>
        <Avatar className={classes.avatar} component={RouterLink} src={`${process.env.REACT_APP_BACKEND_URL}` + user.user.avatar} to="/nh/thong-tin-ca-nhan" />
        <Typography className={classes.name} color="textPrimary" variant="h5">
          {user.user.full_name}
        </Typography>
        <Typography color="textSecondary" variant="body2">
          {user.level || "Sinh viên Đại học"}
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
  onMobileClose: () => { },
  openMobile: false,
};

export default NavBar;
