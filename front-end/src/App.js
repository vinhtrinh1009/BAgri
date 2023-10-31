import React, { Fragment, useEffect } from 'react';
import { useRoutes } from "react-router-dom";
import routes from "src/routes";
import { Provider } from "react-redux";
import store from "src/store";
import { SnackbarProvider } from "notistack";
import { ToastContainer } from 'react-toastify'


const App = () => {
    const routing = useRoutes(routes);

    return (
        <Fragment>
            <Provider store={store}>
                <SnackbarProvider maxSnack={1}>
                    {routing}
                </SnackbarProvider>
            </Provider>
            <ToastContainer />
        </Fragment>
    );
}
export default App