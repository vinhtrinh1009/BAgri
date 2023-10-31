import React, { Fragment, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Container, Row } from "reactstrap";

import { dappActions } from "src/redux/User/DApps/reducer";
import CardDApp from "./components/CardDApp";

import { Button } from "@material-ui/core";
import { useNavigate } from "react-router";
import { AddCircleOutline } from "@material-ui/icons";

const MyDApp = (props) => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const list_dapps = useSelector((state) => state.DApp.list_dapps);

    useEffect(() => {
        dispatch(dappActions.getDApps());
        const interval = setInterval(() => {
            dispatch(dappActions.getDApps());
        }, 5000);
        // dispatch({ type: LAYOUT, payload: localStorage.getItem("layout_version") });
        return () => {
            clearInterval(interval);
        };
    }, []);

    const handleAddDApp = () => {
        navigate("new");
    };

    return (
        <Fragment>
            <Container style={{ maxWidth: "1605px", margin: "0 auto" }}>
                <div style={{ padding: "30px 0px" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "30px" }}>
                        <h4>My DApps</h4>
                        <div className="media-body text-right">
                            <Button color="primary" variant="contained" onClick={() => handleAddDApp()} style={{ textTransform: "none" }}>
                                <AddCircleOutline className="mr-2" />
                                <div>{"New DApp"}</div>
                            </Button>
                        </div>
                    </div>

                    <div>
                        <Row>
                            {list_dapps &&
                                list_dapps.map((value, key) => {
                                    return <CardDApp key={"cardDapp" + key + value.status} data={value} />;
                                })}
                        </Row>
                    </div>
                </div>
            </Container>
        </Fragment>
    );
};

export default MyDApp;
