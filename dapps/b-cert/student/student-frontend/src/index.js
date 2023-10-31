import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter } from "react-router-dom";
import App from "./App";

import axios from "axios";
import { getToken } from "./utils/mng-token";
axios.defaults.baseURL = `${process.env.REACT_APP_BACKEND_URL}/api/v1`;
axios.defaults.headers.common["Authorization"] = getToken();

ReactDOM.render(
  <BrowserRouter>
    <App />
  </BrowserRouter>,
  document.getElementById("root")
);
