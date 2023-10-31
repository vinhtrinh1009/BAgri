import { Navigate, useRoutes } from "react-router-dom";
// layouts

import NotFound from "src/shared/NotFound/Page404";

import DetailSeason from "./views/DetailSeason/DetailSeason";

// ----------------------------------------------------------------------

export default function Router() {
    return useRoutes([
        {
            path: "/seasons/:IdSeason",
            element: <DetailSeason />,
        },
        { path: "404", element: <NotFound /> },
    ]);
}
