import React, { Fragment, useEffect, Suspense } from "react";
import ReactDOM from "react-dom";
import App from "./App";
import * as serviceWorker from "./serviceWorker";
import { BrowserRouter } from "react-router-dom";

import "./index.scss";
import axios from "axios";
import { getToken } from "./utils/token";
import Loader from "src/shared/Loading";

axios.defaults.headers.common["Authorization"] = getToken();

const Root = (props) => {
    const abortController = new AbortController();

    useEffect(() => {
        console.ignoredYellowBox = ["Warning: Each", "Warning: Failed"];
        console.disableYellowBox = true;
        return function cleanup() {
            abortController.abort();
        };
        // eslint-disable-next-line
    }, []);

    return (
        <Fragment>
            <BrowserRouter>
                <Suspense fallback={<Loader />}>
                    <App />
                </Suspense>
            </BrowserRouter>
        </Fragment>
    );
};
ReactDOM.render(<Root />, document.getElementById("root"));

serviceWorker.unregister();
