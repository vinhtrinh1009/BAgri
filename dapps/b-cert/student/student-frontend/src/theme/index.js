import { createMuiTheme, colors } from "@material-ui/core";
import shadows from "./shadows";
import typography from "./typography";
import green from "@material-ui/core/colors/green";
import orange from "@material-ui/core/colors/orange";
import yellow from "@material-ui/core/colors/yellow";
import teal from "@material-ui/core/colors/teal";

const theme = createMuiTheme({
  palette: {
    background: {
      dark: "#F4F6F8",
      default: colors.common.white,
      paper: colors.common.white,
    },
    primary: teal,
    // secondary: "",
    // primary: {
    //   main: colors.indigo[500]
    // },
    // secondary: {
    //   main: colors.indigo[500]
    // },
    text: {
      primary: colors.blueGrey[900],
      secondary: colors.blueGrey[600],
    },
  },
  shadows,
  typography,
});

export default theme;
