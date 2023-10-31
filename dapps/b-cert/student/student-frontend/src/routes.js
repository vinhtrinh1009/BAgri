import React from "react";
import { Navigate } from "react-router-dom";
import DashboardLayout from "src/layouts/DashboardLayout";
import MainLayout from "src/layouts/MainLayout";
import NotFoundView from "src/shared/NotFoundView";
import SignUpView from "src/views/SignUp";
import SignInView from "src/views/SignIn";
import { getToken } from "./utils/mng-token";
import StudentProfile from "./views/StudentProfile";
import Test from "./Test";
import AccountManagement from "./views/AccountManagement";
import ShareCertificate from "./views/ShareCertificate";
import { getRole, ROLE } from "./utils/mng-role";
import ResultStudy from "./views/ResultStudy";

const routes = [
    {
        path: "/student",
        element: <DashboardLayout />,
        children: [
            { path: "thong-tin-ca-nhan", element: <StudentProfile /> },
            { path: "quan-ly-tai-khoan", element: <AccountManagement /> },
            { path: "ket-qua-hoc-tap", element: <ResultStudy /> },
            { path: "chia-se-bang-cap", element: <ShareCertificate /> },
            { path: "*", element: <Navigate to="/404" replace={true} /> },
        ],
    },
    {
        path: "/",
        element: <MainLayout />,
        children: [
            // { path: "dang-ki", element: <SignUpView /> },
            { path: "dang-nhap", element: <SignInView /> },
            { path: "404", element: <NotFoundView /> },
            { path: "/", element: <Redirector /> },
            { path: "*", element: <Navigate to="/404" /> },
        ],
    },
];

function Redirector(props) {
    const role = getRole();
    let to = "/dang-nhap";
    if (!role) {
        to = "/dang-nhap";
    } else if (role === ROLE.STUDENT) {
        to = "/student/thong-tin-ca-nhan";
    }
    return <Navigate to={to} />;
}

export default routes;
