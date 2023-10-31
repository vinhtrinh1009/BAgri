import React from "react";
import Router from "./routes";
import ScrollToTop from "./components/ScrollToTop";
import { Fragment } from "react";

// ----------------------------------------------------------------------

export default function App() {
    // return (
    //   <ThemeConfig>
    //     <ScrollToTop />
    //     <GlobalStyles />
    //     <BaseOptionChartStyle />
    //     <Router />
    //   </ThemeConfig>
    // );

    return (
        <Fragment>
            <ScrollToTop />
            <Router />
        </Fragment>
    );
}
