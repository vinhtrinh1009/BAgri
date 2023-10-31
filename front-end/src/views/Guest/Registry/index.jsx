import React, { useState } from "react";
import { Link as RouterLink, useNavigate } from "react-router-dom";
import { Container, Row, Col, Form, FormGroup, Input, Label, Button } from "reactstrap";

import { useDispatch, useSelector } from "react-redux";
import { getRouteByRole } from "src/utils/role";
import { registry } from "src/services/Guest/registry";
import { OPEN_ERROR_ALERT } from "src/redux/User/Alerts/actionTypes";
import { OPEN_SUCCESS_ALERT } from "src/redux/User/Alerts/actionTypes";
import { OPEN_WARNING_ALERT } from "src/redux/User/Alerts/actionTypes";
import { imagePath } from "../../../constant/imagePath";

const Registry = (props) => {
    const dispatch = useDispatch();
    const [togglePassword, setTogglePassword] = useState(false);

    const [state, setState] = useState({
        email: "",
        username: "",
        password: "",
        full_name: "",
        phone: "",
    });

    const navigate = useNavigate();
    const HideShowPassword = (tPassword) => {
        setTogglePassword(!tPassword);
    };

    async function hdRegistry(e) {
        e.preventDefault();
        try {
            const data_post = {
                username: state.username,
                password: state.password,
                email: state.email,
                full_name: state.full_name,
                phone: state.phone
            };
            if (data_post.email === "") {
                dispatch({ type: OPEN_WARNING_ALERT, payload: { message: "Enter your email, please!" } });
            } else if (data_post.username === "") {
                dispatch({ type: OPEN_WARNING_ALERT, payload: { message: "Enter your username, please!" } });
            } else if (data_post.password === "") {
                dispatch({ type: OPEN_WARNING_ALERT, payload: { message: "Enter your password, please!" } });
            } else if (data_post.full_name === "") {
                dispatch({ type: OPEN_WARNING_ALERT, payload: { message: "Enter your fullname, please!" } });
            } else if (data_post.phone === "") {
                dispatch({ type: OPEN_WARNING_ALERT, payload: { message: "Enter your phone number, please!" } });
            } else {
                const response = await registry(data_post);
                if (response.data.status == "success") {
                    dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Sign Up Success! Let's login now." } });
                    setTimeout(() => {
                        navigate(getRouteByRole("guest"));
                    }, 900);
                } else {
                    dispatch({ type: OPEN_ERROR_ALERT, payload: { message: response.data.data.message } });
                    console.error(response.data);
                }
            }
        } catch (error) {
            dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Registration failed!" } });
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
                                    <img className="img-fluid for-light" src={imagePath.LOGO_LIGHT} height="40" width="125" alt="looginpage" />
                                    <img className="img-fluid for-dark" src={imagePath.LOGO_DARK} height="40" width="125" alt="looginpage" />
                                </a>
                            </div>
                            <div className="login-main">
                                <Form className="theme-form">
                                    <h4>{"Create your account"}</h4>
                                    <p>{"Enter your personal details to create account"}</p>
                                    <FormGroup>
                                        <Label className="col-form-label">{"Email Address"}</Label>
                                        <Input
                                            className="form-control"
                                            type="email"
                                            name="email"
                                            value={state.email}
                                            onChange={(e) => {
                                                setState({ ...state, email: e.target.value });
                                            }}
                                            required
                                        />
                                    </FormGroup>
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
                                    <FormGroup>
                                        <Label className="col-form-label">{"Fullname"}</Label>
                                        <Input
                                            className="form-control"
                                            type="text"
                                            name="full_name"
                                            value={state.full_name}
                                            onChange={(e) => {
                                                setState({ ...state, full_name: e.target.value });
                                            }}
                                            required
                                        />
                                    </FormGroup>
                                    <FormGroup>
                                        <Label className="col-form-label">{"Phone number"}</Label>
                                        <Input
                                            className="form-control"
                                            type="text"
                                            name="phone"
                                            value={state.phone}
                                            onChange={(e) => {
                                                setState({ ...state, phone: e.target.value });
                                            }}
                                            required
                                        />
                                    </FormGroup>
                                    <div className="form-group mb-0">
                                        <div className="checkbox ml-3">
                                            <Input id="checkbox1" type="checkbox" />
                                            <Label className="text-muted" for="checkbox1">
                                                {"Agree with"}
                                                <a className="ml-2" href="#javascript">
                                                    {"PrivacyPolicy"}
                                                </a>
                                            </Label>
                                        </div>
                                        <Button color="primary" className="btn-block" type="submit" onClick={hdRegistry}>
                                            {"Registry"}
                                        </Button>
                                    </div>
                                    {/* <h6 className="text-muted mt-4 or">{"Or signup with"}</h6>
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
                                    <p className="mt-4 mb-0">
                                        {"Already have an account?"}
                                        <a className="ml-2" href="/login">
                                            {"Log In"}
                                        </a>
                                    </p>
                                </Form>
                            </div>
                        </div>
                    </div>
                </Col>
            </Row>
        </Container>
    );
};

export default Registry;
