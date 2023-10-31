import { Card, Container } from "reactstrap";
import React, { Fragment } from "react";
import { useSelector } from "react-redux";
import "./index.scss";
import HeaderSetting from "./components/Header";
import Account from "./components/Account";
import Password from "./components/Password";
import Email from "./components/Email";
import Plan from "./components/Plan";

const Settings = () => {
    const category = useSelector((state) => state.Setting.category);

    return (
        <Fragment>
            <Container style={{ maxWidth: "1605px", margin: "0 auto" }}>
                <div style={{ padding: "30px 0px" }}>
                    <div style={{ marginBottom: "24px" }}>
                        <h4 className="title">Settings</h4>
                    </div>

                    <Card className="bodySetting">
                        <HeaderSetting />
                        <hr />
                        {category === "account" ? (
                            <Account />
                        ) : category === "password" ? (
                            <Password />
                        ) : category === "email" ? (
                            <Email />
                        ) : (
                            // : category === "notification" ? (
                            //     <Notifications />
                            // )
                            // category === "plan" ? (
                            //     <Plan />
                            // ) :
                            ""
                        )}
                    </Card>
                </div>
            </Container>
        </Fragment>
    );
};

export default Settings;
