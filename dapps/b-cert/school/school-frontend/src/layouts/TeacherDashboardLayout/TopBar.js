import { AppBar, Badge, Box, Hidden, IconButton, makeStyles, Menu, MenuItem, Toolbar } from "@material-ui/core";
import InputIcon from "@material-ui/icons/Input";
import MenuIcon from "@material-ui/icons/Menu";
import NotificationsIcon from "@material-ui/icons/NotificationsOutlined";
import clsx from "clsx";
import PropTypes from "prop-types";
import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { Link as RouterLink, useNavigate } from "react-router-dom";
import Logo from "src/shared/Logo";
import { resetStore } from "../../store";
import { clearToken } from "src/utils/mng-token";
import { clearRole } from "../../utils/mng-role";
import { setPrivateKeyHex } from "../../utils/keyholder";
import PersonOutlineIcon from "@material-ui/icons/PersonOutline";
import Fade from "@material-ui/core/Fade";
import TwoFactorAuthenDialog from "./TwoFactorAuthenDialog";

const useStyles = makeStyles(() => ({
  root: {},
  avatar: {
    width: 60,
    height: 60,
  },
}));

const TopBar = ({ className, onMobileNavOpen, ...rest }) => {
  const classes = useStyles();
  const [notifications] = useState([]);
  // user settings menu....
  const [menuAnchorEl, setMenuAnchorEl] = React.useState(null);
  const [openDialog, setOpenDialog] = useState(false);

  const navigate = useNavigate();
  const dp = useDispatch();

  return (
    <AppBar className={clsx(classes.root, className)} elevation={0} {...rest}>
      <Toolbar>
        <RouterLink to="/">
          <Logo />
        </RouterLink>
        <Box flexGrow={1} />
        <Hidden mdDown>
          <IconButton color="inherit">
            <Badge badgeContent={notifications.length} color="primary" variant="dot">
              <NotificationsIcon />
            </Badge>
          </IconButton>

          <IconButton
            color="inherit"
            onClick={(e) => {
              clearToken();
              clearRole();
              setPrivateKeyHex(null);
              dp(resetStore());
              navigate("/");
            }}
          >
            <InputIcon />
          </IconButton>

          <IconButton color="inherit" onClick={(event) => setMenuAnchorEl(event.currentTarget)}>
            <PersonOutlineIcon></PersonOutlineIcon>
          </IconButton>
          <Menu
            anchorEl={menuAnchorEl}
            keepMounted
            open={Boolean(menuAnchorEl)}
            onClose={() => setMenuAnchorEl(null)}
            TransitionComponent={Fade}
          >
            <MenuItem>Đổi mật khẩu</MenuItem>

            <MenuItem
              onClick={() => {
                setOpenDialog(true);
                setMenuAnchorEl(null);
              }}
            >
              Cài đặt xác thực 2 bước
            </MenuItem>
          </Menu>
          {openDialog && <TwoFactorAuthenDialog setOpenDialog={setOpenDialog}></TwoFactorAuthenDialog>}
        </Hidden>
        <Hidden lgUp>
          <IconButton color="inherit" onClick={onMobileNavOpen}>
            <MenuIcon />
          </IconButton>
        </Hidden>
      </Toolbar>
    </AppBar>
  );
};

TopBar.propTypes = {
  className: PropTypes.string,
  onMobileNavOpen: PropTypes.func,
};

export default TopBar;
