import React from "react";
import { Navigate } from "react-router-dom";
import MainLayout from "src/layouts/MainLayout";
import NotFoundView from "src/shared/NotFoundView";
import ValidateToken from "src/views/ValidateToken";
import VerifyData from "src/views/VerifyData";

const routes = [
    {
        path: "/",
        element: <MainLayout />,
        children: [
            { path: "xac-thuc", element: <ValidateToken /> },
            { path: "ket-qua/:token", element: <VerifyData /> },
            { path: "404", element: <NotFoundView /> },
            { path: "/", element: <Navigate to="xac-thuc" /> },
            { path: "*", element: <Navigate to="/404" /> },
        ],
    },
];

export default routes;
