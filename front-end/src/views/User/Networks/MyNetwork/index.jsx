import { Button } from "@material-ui/core";
import React, { Fragment, useEffect } from "react";
import { Container, Row } from "reactstrap"; //
import CardNetwork from "./components/CardNetwork";
import { useDispatch, useSelector } from "react-redux";
import { networkActions } from "src/redux/User/Networks/reducer";
import { AddCircleOutline } from "@material-ui/icons";
import { useNavigate } from "react-router";

export default function MyNetwork() {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const list_network = useSelector((state) => state.Network.list_network);

    useEffect(() => {
        dispatch(networkActions.getNetwork({}));
        const interval = setInterval(() => dispatch(networkActions.getNetwork({})), 5000);
        return () => {
            clearInterval(interval);
        };
    }, []);

    const handleAddNetwork = () => {
        navigate("new");
    };

    return (
        <Fragment>
            <Container style={{ maxWidth: "1605px", margin: "0 auto" }}>
                <div style={{ padding: "30px 0px" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "30px" }}>
                        <h4>My Networks</h4>
                        <div className="media-body text-right">
                            <Button color="primary" variant="contained" onClick={() => handleAddNetwork()} style={{ textTransform: "none" }}>
                                <AddCircleOutline className="mr-2" /> {"New Network"}
                            </Button>
                        </div>
                    </div>

                    <div>
                        <Row>
                            {list_network &&
                                list_network.map((value, key) => {
                                    return <CardNetwork key={"cardnetwork" + key + value.status} data={value} />;
                                })}
                        </Row>
                    </div>
                </div>
            </Container>
        </Fragment>
    );
}
