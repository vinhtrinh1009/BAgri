import "react-perfect-scrollbar/dist/css/styles.css";
import { useRoutes } from "react-router-dom";
import { ThemeProvider } from "@material-ui/core";
import GlobalStyles from "src/shared/GlobalStyles";
import theme from "src/theme";
import routes from "src/routes";
import { Provider } from "react-redux";
import store from "./store";
import { SnackbarProvider } from "notistack";

const App = () => {
  const routing = useRoutes(routes);

  return (
    <ThemeProvider theme={theme}>
      <GlobalStyles />
      <Provider store={store}>
        <SnackbarProvider maxSnack={1}>{routing}</SnackbarProvider>
      </Provider>
    </ThemeProvider>
  );
};

export default App;
