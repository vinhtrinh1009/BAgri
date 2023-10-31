import Avatar from "@material-ui/core/Avatar";
import Box from "@material-ui/core/Box";
import Button from "@material-ui/core/Button";
import Container from "@material-ui/core/Container";
import CssBaseline from "@material-ui/core/CssBaseline";
import Grid from "@material-ui/core/Grid";
import Link from "@material-ui/core/Link";
import { makeStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
import Typography from "@material-ui/core/Typography";
import LockOutlinedIcon from "@material-ui/icons/LockOutlined";
import { Alert } from "@material-ui/lab";
import axios from "axios";
import React, { useState } from "react";
import { Link as RouterLink, useNavigate } from "react-router-dom";



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
    marginTop: theme.spacing(3),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

export default function SignUp() {
  const classes = useStyles();

  const [state, setState] = useState({
    email: "",
    password: "",
    repassword: "",
  });


  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState(null);
  const navigate = useNavigate();
  

  async function hdSubmit(e) {
    e.preventDefault();
    if (state.username && state.email && state.password && state.first_name && state.last_name) {
      try {
        console.log(state);
        const response = await axios.post("/auth/register", state);
        // console.log(response)
        // const result = response.data;
        // setLocalToken(result.token);
        // setLocalRole(result.role);
        // setRemember(true);
        // setErrors(null);
        setSuccess("Đăng kí tài khoản thành công!");
        setTimeout(() => navigate("/dang-nhap", 1000));
      } catch (error) {
        console.log(error);
        setErrors(error.response.data);
      }
    } else {
      if (!state.username) setErrors({...errors, username: "Phải nhập user name!"});
      if (!state.email) setErrors({...errors, email: "Phải nhập email!"});
      if (!state.password) setErrors({...errors, password: "Phải nhập password!"});
      if (!state.first_name) setErrors({...errors, first_name: "Phải nhập first name!"});
      if (!state.last_name) setErrors({...errors, last_name: "Phải nhập last name!"});
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
          Đăng kí tài khoản Trường học
        </Typography>
        <div>
          {success ? (
            <Alert className={classes.alert} severity="success">
              {success}
            </Alert>
          ) : null}
        </div>
        <form className={classes.form} noValidate>
          <Grid container spacing={2}>
          <Grid item xs={12}>
              <TextField
                variant="outlined"
                required
                fullWidth
                id="username"
                label="User Name"
                value={state.username}
                onChange={(e) => {
                  setState({ ...state, username: e.target.value });
                  setErrors(null);
                }}
                error={Boolean(errors?.username)}
                helperText={errors?.username}
                disabled={Boolean(success)}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                variant="outlined"
                required
                fullWidth
                id="email"
                label="Email"
                value={state.email}
                onChange={(e) => {
                  setState({ ...state, email: e.target.value });
                  setErrors(null);
                }}
                error={Boolean(errors?.email)}
                helperText={errors?.email}
                disabled={Boolean(success)}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                variant="outlined"
                required
                fullWidth
                label="Mật khẩu"
                type="password"
                id="password"
                value={state.password}
                onChange={(e) => {
                  setState({ ...state, password: e.target.value });
                  setErrors(null);
                }}
                error={Boolean(errors?.password)}
                helperText={errors?.password}
                disabled={Boolean(success)}
              />
              
            </Grid>
            
            {/* <Grid item xs={12}>
              <TextField
                variant="outlined"
                required
                fullWidth
                label="Nhập lại mật khẩu"
                type="password"
                id="rePassword"
                value={state.repassword}
                onChange={(e) => {
                  setState({ ...state, repassword: e.target.value });
                  setErrors(null);
                }}
                error={Boolean(errors?.repassword)}
                helperText={errors?.repassword}
                disabled={Boolean(success)}
              />
            </Grid> */}
            <Grid item xs={12}>
              <TextField
                variant="outlined"
                required
                fullWidth
                id="firstName"
                label="First Name"
                value={state.first_name}
                onChange={(e) => {
                  setState({ ...state, first_name: e.target.value });
                  setErrors(null);
                }}
                error={Boolean(errors?.first_name)}
                helperText={errors?.first_name}
                disabled={Boolean(success)}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                variant="outlined"
                required
                fullWidth
                id="lastName"
                label="Last Name"
                value={state.last_name}
                onChange={(e) => {
                  setState({ ...state, last_name: e.target.value });
                  setErrors(null);
                }}
                error={Boolean(errors?.last_name)}
                helperText={errors?.last_name}
                disabled={Boolean(success)}
              />
            </Grid>
          </Grid>
          <Button type="submit" fullWidth variant="contained" color="primary" className={classes.submit} onClick={hdSubmit}>
            Đăng kí
          </Button>
          <Grid container justify="flex-end">
            <Grid item>
              <Link component={RouterLink} to="/dang-nhap">
                Bạn đã có tài khoản rồi? Đăng nhập
              </Link>
            </Grid>
          </Grid>
        </form>
      </div>
      <Box mt={5}>
        <Copyright />
      </Box>
    </Container>
  );
}
