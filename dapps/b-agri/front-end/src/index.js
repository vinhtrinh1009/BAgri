// scroll bar
import "simplebar/src/simplebar.css";

import ReactDOM from "react-dom";
import { BrowserRouter } from "react-router-dom";
import { HelmetProvider } from "react-helmet-async";

//
import App from "./App";
import * as serviceWorker from "./serviceWorker";

import "./index.scss";
// ----------------------------------------------------------------------

ReactDOM.render(
    <BrowserRouter>
        <App />
    </BrowserRouter>,
    document.getElementById("root")
);

// If you want to enable client cache, register instead.
serviceWorker.unregister();
