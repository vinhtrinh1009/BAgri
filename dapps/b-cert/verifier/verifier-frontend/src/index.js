import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import axios from "axios";

axios.defaults.baseURL = `${process.env.REACT_APP_BACKEND_URL}/api/v1/`;

ReactDOM.render(
  <BrowserRouter>
    <App />
  </BrowserRouter>,
  document.getElementById("root")
);
