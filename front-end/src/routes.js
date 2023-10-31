import React from "react";
import { Navigate } from "react-router-dom";
import { getRole, ROLE } from "src/utils/role";

// Guest view
import Login from "src/views/Guest/Login";
import Registry from "src/views/Guest/Registry";

// Network
import MyNetwork from "./views/User/Networks/MyNetwork";
import NewNetwork from "./views/User/Networks/NewNetwork";
import DetailNetwork from "./views/User/Networks/DetailNetwork";

// DApps
import MyDApp from "src/views/User/DApps/MyDApp";
import NewDApp from "src/views/User/DApps/NewDApp";
import DetailDApp from "./views/User/DApps/DetailDApp";

// Tokens
import MyTokensPage from './views/User/Tokens/MyTokensPage';
import NewTokenPage from './views/User/Tokens/NewTokenPage';
import TokenDetailPage from './views/User/Tokens/TokenDetailPage';
import TransferTokenPage from './views/User/Tokens/TransferTokenPage';
import InspectTokenPage from "./views/User/Tokens/InspectTokenPage";

// Storages
import MyStorage from "./views/User/Storages2/MyStorage/MyStorage";
import DetailFolder from "./views/User/Storages2/DetailFolder/DetailFolder";
import Recent from "./views/User/Storages2/Recent/Recent";
import Favorite from "./views/User/Storages2/Favorite/Favorite";
import Trash from "./views/User/Storages2/Trash/Trash";
import ShareWithMe from "./views/User/Storages2/ShareWithMe/ShareWithMe";
import DetailPlatfromFolder from "./views/User/Storages2/DetailPlatformFolder/DetailPlatformFolder";

// Settings
import Settings from "src/views/User/Settings";

import NotFound from "src/shared/NotFound";

import Verify from "src/views/User/Settings/components/Verify";
import EditDApp from "./views/User/DApps/EditDApp/EditDApp";

// Layout
import GuestLayout from "src/layouts/GuestLayout";
const UserLayout = React.lazy(() => import("./layouts/UserLayout/UserLayout"));

const routes = [
    {
        path: "/networks",
        element: <UserLayout />,
        children: [
            { path: "", element: <MyNetwork /> },
            { path: "new", element: <NewNetwork /> },
            { path: ":networkId", element: <DetailNetwork /> },
            { path: "*", element: <Navigate to="/networks" replace={true} /> },
            // { path: "404", element: <NotFound /> },
        ],
    },
    {
        path: "/dapps",
        element: <UserLayout />,
        children: [
            { path: "", element: <MyDApp /> },
            { path: "new", element: <NewDApp /> },
            { path: ":dappId", element: <DetailDApp /> },
            { path: "edit/:dappId", element: <EditDApp /> },
            { path: "*", element: <Navigate to="/dapps" replace={true} /> },
            // { path: "404", element: <NotFound /> },
        ],
    },
    {
        path: "/tokens",
        element: <UserLayout />,
        children: [
            {path: "", element: <MyTokensPage/>},
            {path: "new", element: <NewTokenPage/>},
            {path: "transfer", element: <TransferTokenPage/>},
            {path: ":tokenid/:token_type", element: <TokenDetailPage/>},
            {path: "inspect", element: <InspectTokenPage/>},
            { path: "*", element: <Navigate to="/tokens" replace={true} /> },
            // { path: "404", element: <NotFound /> },
        ],
    },
    {
        path: "/storages",
        element: <UserLayout />,
        children: [
            { path: "", element: <MyStorage /> },
            { path: ":folderId", element: <DetailFolder /> },
            { path: "platform-artifact", element: <ShareWithMe /> },
            { path: "platform-artifact/:folderId", element: <DetailPlatfromFolder /> },
            { path: "recent", element: <Recent /> },
            { path: "favorite", element: <Favorite /> },
            { path: "trash", element: <Trash /> },
            { path: "*", element: <Navigate to="/storages" replace={true} /> },
            // { path: "404", element: <NotFound /> }
        ],
    },
    {
        path: "/settings",
        element: <UserLayout />,
        children: [
            { path: "", element: <Settings /> },
            { path: ":userId/verify/email", element: <Verify /> },
            { path: ":userId/verify/password", element: <Verify /> },
            // { path: "*", element: <Navigate to="/settings/404" replace={true} /> },
            { path: "*", element: <Navigate to="/settings" replace={true} /> },
            // { path: "404", element: <NotFound /> }
        ],
    },
    {
        path: "/",
        element: <GuestLayout />,

        children: [
            { path: "login", element: <Login /> },
            // { path: "registry", element: <Registry /> },
            // {path: "forgot-password", element: <ForgotPassword />},
            { path: "*", element: <Redirector /> },
            // { path: "404", element: <NotFound /> },
            { path: "/", element: <Redirector /> },
        ],
    },
];

function Redirector(props) {
    const role = getRole();
    let to = "";
    if (!role) {
        to = "/login";
    } else if (role === ROLE.USER) {
        to = "/dapps";
    }
    return <Navigate to={to} />;
}

export default routes;
