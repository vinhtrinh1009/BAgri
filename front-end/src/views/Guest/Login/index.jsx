import React, { useState } from "react";
import { Link as RouterLink, useNavigate } from "react-router-dom";
import { Container, Row, Col, Form, FormGroup, Input, Label, Button } from "reactstrap";
// import { Twitter, Facebook, GitHub } from 'react-feather'
// import Logo from 'src/assets'

import { useDispatch, useSelector } from "react-redux";
import { login } from "src/services/Guest/login";
import { setLocalToken, setRemember, setSessionToken } from "src/utils/token";
import { getRouteByRole, setLocalRole, setSessionRole } from "src/utils/role";
import { setLocalUser, setSessionUser } from "src/utils/user";
import { OPEN_ERROR_ALERT } from "src/redux/User/Alerts/actionTypes";
import { OPEN_WARNING_ALERT } from "src/redux/User/Alerts/actionTypes";
import { OPEN_SUCCESS_ALERT } from "src/redux/User/Alerts/actionTypes";
import { imagePath } from "../../../constant/imagePath";

const Login = (props) => {
    const dispatch = useDispatch();

    const [togglePassword, setTogglePassword] = useState(false);
    const user = useSelector((state) => state.User.user);
    const [state, setState] = useState({
        username: "",
        password: "",
        remember: true,
    });

    const navigate = useNavigate();

    const HideShowPassword = (tPassword) => {
        setTogglePassword(!tPassword);
    };

    async function hdLogin(e) {
        e.preventDefault();
        try {
            const data = {
                username: state.username,
                password: state.password,
            };
            if (data.email === "") {
                dispatch({ type: OPEN_WARNING_ALERT, payload: { message: "Enter your email, please!" } });
            } else if (data.username === "") {
                dispatch({ type: OPEN_WARNING_ALERT, payload: { message: "Enter your user name, please!" } });
            } else {
                const response = await login(data);
                const body = response.data;
                if (body.status == "success") {
                    if (state.remember) {
                        setLocalToken(body.data.token);
                        setLocalRole("user");
                        setLocalUser(body.data.user_id);
                        setRemember(true);
                        // localStorage.setItem("user", JSON.stringify(body.data.user));
                    } else {
                        setSessionToken(body.data.token);
                        setSessionRole("user");
                        setSessionUser(body.data.user_id);
                        setRemember(false);
                    }
                    // await dispatch(userActions.getProfile({ user_id: body.data.user_id }));
                    dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Logged in successfully!" } });
                    setTimeout(() => {
                        navigate(getRouteByRole("user"));
                    }, 900);
                } else {
                    dispatch({ type: OPEN_ERROR_ALERT, payload: { message: body.data.message } });
                    console.error(body);
                }
            }
        } catch (error) {
            dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Login error!" } });
            console.error(error);
        }
    }

    return (
        <Container fluid={true} className="p-0">
            <Row>
                <Col xs="12">
                    <div className="login-card">
                        <div>
                            <div>
                                <a className="logo" href="#javascript">
                                    <img className="img-fluid " src={imagePath.LOGO_LIGHT} height="40" width="125" alt="" />
                                    {/* <img className="img-fluid for-dark" src={imagePath.LOGO_DARK} height="40" width="125" alt="" /> */}
                                </a>
                            </div>
                            <div className="login-main">
                                <Form className="theme-form">
                                    <h4>{"Login V-chain Platform"}</h4>
                                    <p></p>
                                    <FormGroup>
                                        <Label className="col-form-label">{"Username"}</Label>
                                        <Input
                                            className="form-control"
                                            type="text"
                                            name="username"
                                            value={state.username}
                                            onChange={(e) => {
                                                setState({ ...state, username: e.target.value });
                                            }}
                                            required
                                        />
                                    </FormGroup>
                                    <FormGroup>
                                        <Label className="col-form-label">{"Password"}</Label>
                                        <Input
                                            className="form-control"
                                            type={togglePassword ? "text" : "password"}
                                            name="password"
                                            value={state.password}
                                            onChange={(e) => {
                                                setState({ ...state, password: e.target.value });
                                            }}
                                            required
                                        />
                                        <div className="show-hide" onClick={() => HideShowPassword(togglePassword)}>
                                            <span className={togglePassword ? "" : "show"}></span>
                                        </div>
                                    </FormGroup>
                                    <div className="form-group mb-0">
                                        <div className="checkbox ml-3">
                                            <Input
                                                id="checkbox1"
                                                type="checkbox"
                                                name="remember"
                                                checked={state.remember}
                                                onChange={(e) => {
                                                    setState({ ...state, remember: !state.remember });
                                                }}
                                            />
                                            <Label className="text-muted" for="checkbox1">
                                                Remember me
                                            </Label>
                                        </div>
                                        <a className="link" href="#javascript"></a>
                                        <Input type="submit" color="primary" className="btn btn-primary" onClick={hdLogin} value="Login"></Input>
                                    </div>
                                    {/* <h6 className="text-muted mt-4 or">{"Or Sign in with"}</h6>
                                        <div className="social mt-4">
                                            <div className="btn-showcase">
                                            <Button color="light">
                                                <Facebook className="txt-fb" />
                                            </Button>
                                            <Button color="light">
                                                <i className="icon-social-google txt-googleplus"></i>
                                            </Button>
                                            <Button color="light">
                                                <Twitter className="txt-twitter" />
                                            </Button>
                                            <Button color="light">
                                                <GitHub />
                                            </Button>
                                            </div>
                                        </div> */}
                                    {/* <p className="mt-4 mb-0">
                                        {"Don't have account?"}
                                        <a className="ml-2" href="/registry">
                                            {"CreateAccount"}
                                        </a>
                                    </p> */}
                                </Form>
                            </div>
                        </div>
                    </div>
                </Col>
            </Row>
        </Container>
    );
};

export default Login;
