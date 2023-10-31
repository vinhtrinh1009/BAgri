import React from "react";
import { Link as RouterLink } from "react-router-dom";
import clsx from "clsx";
import PropTypes from "prop-types";
import { AppBar, Toolbar, makeStyles } from "@material-ui/core";
import Logo from "src/shared/Logo";
import { Typography } from "@material-ui/core";
import { size } from "lodash";

const useStyles = makeStyles({
  root: {},
  toolbar: {
    height: 64,
  },
  title: {
    width: '100%',
    textAlign: "center",
    color: 'white',
    fontSize: "larger"
  }
});

const TopBar = ({ className, ...rest }) => {
  const classes = useStyles();

  return (
    <AppBar className={clsx(classes.root, className)} elevation={0} {...rest}>
      <Toolbar className={classes.toolbar}>
        <RouterLink to="/">
          <Logo />
        </RouterLink>
        <Typography className={classes.title}>
          Hệ Thống Xác Thực Bằng Cấp
        </Typography>
      </Toolbar>
    </AppBar>
  );
};

TopBar.propTypes = {
  className: PropTypes.string,
};

export default TopBar;
