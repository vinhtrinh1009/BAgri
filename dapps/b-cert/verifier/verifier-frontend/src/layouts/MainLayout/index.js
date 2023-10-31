import React from "react";
import { Outlet } from "react-router-dom";
import { makeStyles } from "@material-ui/core";
import TopBar from "./TopBar";
import PerfectScrollbar from "react-perfect-scrollbar";

const useStyles = makeStyles((theme) => ({
  root: {
    height: "100%",
    width: "100%",
    overflow: "hidden",
    display: "flex",
    // backgroundColor: theme.palette.background.default,
    backgroundColor: theme.palette.background.dark,
  },
  wrapper: {
    flex: "1 1 auto",
    overflow: "hidden",
    display: "flex",
    paddingTop: 64,
  },
  contentContainer: {
    flex: "1 1 auto",
    overflow: "hidden",
    display: "flex",
  },
  content: {
    flex: "1 1 auto",
    height: "100%",
    overflow: "auto",
  },
}));

const MainLayout = () => {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <TopBar />
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
  );
};

export default MainLayout;
