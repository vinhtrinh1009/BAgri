import { makeStyles } from "@material-ui/core";
import PropTypes from "prop-types";
import React, { forwardRef } from "react";
import { Helmet } from "react-helmet";

const useStyles = makeStyles((theme) => ({
  root: {
    height: "100%",
    padding: theme.spacing(2.5),
  },
}));

const Page = forwardRef(({ children, title = "", ...rest }, ref) => {
  const cls = useStyles();

  return (
    <div ref={ref} {...rest} className={cls.root}>
      <Helmet>
        <title>{title}</title>
      </Helmet>
      {children}
    </div>
  );
});

Page.propTypes = {
  children: PropTypes.node.isRequired,
  title: PropTypes.string,
};

export default Page;
