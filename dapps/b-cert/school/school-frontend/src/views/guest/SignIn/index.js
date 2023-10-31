import Avatar from "@material-ui/core/Avatar";
import Box from "@material-ui/core/Box";
import Button from "@material-ui/core/Button";
import Checkbox from "@material-ui/core/Checkbox";
import Container from "@material-ui/core/Container";
import CssBaseline from "@material-ui/core/CssBaseline";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Grid from "@material-ui/core/Grid";
import Link from "@material-ui/core/Link";
import { makeStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
import Typography from "@material-ui/core/Typography";
import LockOutlinedIcon from "@material-ui/icons/LockOutlined";
import axios from "axios";
import React, { useState } from "react";
import { Link as RouterLink, NavLink, useNavigate } from "react-router-dom";
import { setLocalUniversity, setSessionUniversity, setLocalUser, setSessionUser } from "src/utils/mng_user"
import { setLocalToken, setRemember, setSessionToken } from "src/utils/mng-token";
import { getRouteByRole, setLocalRole, setSessionRole } from "../../../utils/mng-role";
import { useSnackbar } from "notistack"
import { ERR_TOP_CENTER } from "../../../utils/snackbar-utils";

function Copyright() {
  return (
    <Typography variant="body2" color="textSecondary" align="center">
      {"Copyright © "}
      <Link component={RouterLink} to="/">
        B4E Website
      </Link>{" "}
      {new Date().getFullYear()}
      {"."}
    </Typography>
  );
}

const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  alert: {
    marginTop: theme.spacing(3),
  },
  form: {
    width: "100%", // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
  link: {
    color: theme.palette.primary.main,
  },
}));

export default function SignIn() {
  const classes = useStyles();
  const [state, setState] = useState({
    username: "",
    password: "",
    remember: true,
  });
  const [errors, setErrors] = useState(null);
  const navigate = useNavigate();
  const { enqueueSnackbar, closeSnackbar } = useSnackbar();
  
  if (localStorage.getItem("role") != null) {
    window.location.href = getRouteByRole(localStorage.getItem("role"));
  }

  async function hdSubmit(e) {
    e.preventDefault();
    try {
      const response = await axios.post("/auth/login", { username: state.username, password: state.password });
      const body = response.data;
      if (body.role === "student"){
          enqueueSnackbar("ban khong co quyen dang nhap tu trang nay", ERR_TOP_CENTER)
          navigate('/dang-nhap')
      }
      else if (state.remember) {
        setLocalToken(body.access);
        setLocalRole(body.role);
        setLocalUser(body.user)
        setLocalUniversity(body.university)
        setRemember(true);
        navigate(getRouteByRole(body.role));
      } else {
        setSessionToken(body.token);
        setSessionRole(body.role);
        setSessionUser(body.user)
        setSessionUniversity(body.university)
        setRemember(false);
        navigate(getRouteByRole(body.role));
      }
    } catch (error) {
    //   setErrors(error.response.data);
        enqueueSnackbar("Ten dang nhap hoac mat khau khong dung", ERR_TOP_CENTER)
        navigate("/dang-nhap")
    }
  }

  return (
    
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <div className={classes.paper}>
        <Avatar className={classes.avatar}>
          <LockOutlinedIcon />
        </Avatar>
        <Typography component="h1" variant="h3">
          Đăng nhập
        </Typography>
        <form className={classes.form} noValidate>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="username"
            label="Username"
            name="username"
            autoComplete="username"
            autoFocus
            value={state.username}
            onChange={(e) => {
              setState({ ...state, username: e.target.value });
              setErrors({ ...errors, username: null });
            }}
            error={Boolean(errors?.username)}
            helperText={errors?.username}
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="password"
            label="Mật khẩu"
            type="password"
            id="password"
            autoComplete="password"
            value={state.password}
            onChange={(e) => {
              setState({ ...state, password: e.target.value });
              setErrors({ ...errors, password: null });
            }}
            error={Boolean(errors?.password)}
            helperText={errors?.password}
          />
          <FormControlLabel
            control={
              <Checkbox checked={state.remember} onChange={(e) => setState({ ...state, remember: !state.remember })} color="primary" />
            }
            label="Nhớ đăng nhập"
          />
          <Button type="submit" fullWidth variant="contained" color="primary" className={classes.submit} onClick={hdSubmit}>
            Đăng nhập
          </Button>
          <Grid container justify="flex-end">
            
            <Grid item xs={12} md={4}>
              <Typography align="left">
                <Link componet={RouterLink} to="#" variant="body2">
                  Quên mật khẩu?
                </Link>
              </Typography>
            </Grid>
            <Grid item xs={12} md={8}>
              <Typography align="right">
                <Link component={RouterLink} to="/dang-ki" variant="body2">
                  {"Chưa có tài khoản? Đăng kí!"}
                </Link>
              </Typography>
            </Grid>
          </Grid>
        </form>
      </div>
      <Box mt={6}>
        <Copyright />
      </Box>
    </Container>
  );
}
