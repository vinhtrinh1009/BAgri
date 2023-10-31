import { createMuiTheme, colors } from "@material-ui/core";
import shadows from "./shadows";
import typography from "./typography";
import cyan from "@material-ui/core/colors/cyan";
import green from "@material-ui/core/colors/green";
const theme = createMuiTheme({
  palette: {
    background: {
      dark: "#F4F6F8",
      default: colors.common.white,
      paper: colors.common.white,
    },
    primary: green,
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
