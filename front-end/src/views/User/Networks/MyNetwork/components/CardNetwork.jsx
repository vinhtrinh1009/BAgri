import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Link } from "react-router-dom";
import { Row, Col, Card, CardHeader, CardFooter, Badge, CardBody } from "reactstrap";
import { VIEW_MORE } from "src/redux/User/Networks/actionTypes";
import { Button } from "@material-ui/core";
import { useNavigate } from "react-router";
import { imagePath } from "../../../../../constant/imagePath";
import { statusNetworkClassName } from "../../../../../constant/statusNetworkClassName";
import { networkStatus } from "../../../../../constant/networkStatus";
import { ButtonGroup } from "@mui/material";
import { retryCreateNetwork } from "../../../../../services/User/networks";
import { OPEN_SUCCESS_ALERT } from "../../../../../redux/User/Alerts/actionTypes";
import { OPEN_ERROR_ALERT } from "../../../../../redux/User/Alerts/actionTypes";
import { deleteNetwork } from "../../../../../services/User/networks";
import { retryUpdateNetwork } from "../../../../../services/User/networks";
import { rollbackNetwork } from "../../../../../services/User/networks";

const CardNetwork = (prop) => {
    const engineBlockchain = useSelector((state) => state.Network.engineBlockchain);
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const sumPeers = (props) => {
        let temp = 0;
        if (props.data.blockchain_type === "sawtooth") return props.data.blockchain_peer_config.number_peer;
        else {
            props.data.blockchain_peer_config.organizations &&
                props.data.blockchain_peer_config.organizations.map((value, key) => {
                    temp += parseInt(value.number_peer);
                });
            props.data.blockchain_peer_config.organization &&
                props.data.blockchain_peer_config.organization.map((value, key) => {
                    temp += parseInt(value.number_peer);
                });
            return temp;
        }
    };
    const handleExplorer = () => {
        window.open("https://" + prop.data.explorer_url, "_blank");
    };
    function padLeadingZeros(num, size) {
        var s = num + "";
        while (s.length < size) s = "0" + s;
        return s;
    }
    async function reCreateNetwork(idNetwork) {
        const res = await retryCreateNetwork(idNetwork);
        if (res.status != 400) {
            dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Send request success!" } });
        } else {
            dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Send request fail!\n" + res.error } });
        }
    }
    async function reUpdateNetwork(idNetwork) {
        const res = await retryUpdateNetwork(idNetwork);
        if (res.status != 400) {
            dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Send request success!" } });
        } else {
            dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Send request fail!\n" + res.error } });
        }
    }
    async function rollbacknetwork(idNetwork) {
        const res = await rollbackNetwork(idNetwork);
        if (res.status != 400) {
            dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Send request success!" } });
        } else {
            dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Send request fail!\n" + res.error } });
        }
    }
    async function deletenetwork(idNetwork) {
        const res = await deleteNetwork(idNetwork);
        if (res.status != 400) {
            dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Send request success!" } });
        } else {
            dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Send request fail!\n" + res.error } });
        }
    }

    return (
        <Col xl={4} md={6}>
            <Card style={{ boxShadow: "0px 3px 12px #0000001A" }}>
                <CardBody style={{ border: "none", padding: "21px 24px" }}>
                    <Row>
                        <Col xs={5}>
                            <img
                                className="img-50"
                                src={
                                    prop.data.blockchain_type == "fabric"
                                        ? imagePath.fabric
                                        : prop.data.blockchain_type == "sawtooth"
                                        ? imagePath.sawtooth
                                        : prop.data.blockchain_type == "ethereum" && prop.data.node_infrastructure.name == "bsc"
                                        ? imagePath.bsc
                                        : prop.data.blockchain_type == "ethereum" && prop.data.node_infrastructure.name == "bsct"
                                        ? imagePath.bsc
                                        : prop.data.blockchain_type == "ethereum" && prop.data.node_infrastructure.name == "ftm"
                                        ? imagePath.ftm
                                        : prop.data.blockchain_type == "ethereum" && prop.data.node_infrastructure.name == "ftmt"
                                        ? imagePath.ftm
                                        : imagePath.ethereum
                                }
                            />
                            {/* <img className="img-50" src={imagePath[prop.data.blockchain_type] || imagePath.fabric} /> */}
                        </Col>
                        <Col xs={7}>
                            <div
                                style={{
                                    textTransform: "capitalize",
                                    font: "normal normal bold 20px/24px Roboto",
                                    fontWeight: "bold",
                                    overflow: "hidden",
                                    textOverflow: "ellipsis",
                                    whiteSpace: "nowrap",
                                    textAlign: "right",
                                    marginBottom: "8px",
                                }}
                            >
                                {prop.data.name}
                            </div>
                            <div className="state" style={{ justifyContent: "right" }}>
                                <div className={`dot-notify ${statusNetworkClassName[prop.data.status] || statusNetworkClassName.ELSE}`}></div>
                                <div>{networkStatus[prop.data.status] || networkStatus.ELSE}</div>
                            </div>
                        </Col>
                    </Row>
                    <div className="mt-3">
                        <span className="badge">{`${prop.data.blockchain_type} `}</span>
                        <span className="badge">{`${prop.data.consensus}`}</span>
                    </div>
                    <hr />

                    {prop.data.blockchain_type !== "ethereum" ? (
                        <Row className="details">
                            <Col xs="6">
                                <div style={{ font: "normal normal normal 12px/14px Roboto", opacity: "0.5" }}>NODE</div>
                                <div style={{ font: "normal normal 900 24px/28px Roboto" }}>{padLeadingZeros(prop.data.node_infrastructure.number_vm_nodes, 2)}</div>
                            </Col>
                            <Col xs="6">
                                <div style={{ font: "normal normal normal 12px/14px Roboto", opacity: "0.5" }}>PEER</div>
                                <div style={{ font: "normal normal 900 24px/28px Roboto" }}>{padLeadingZeros(sumPeers(prop), 2)}</div>
                            </Col>
                        </Row>
                    ) : (
                        <div style={{ height: "42px" }}></div>
                    )}

                    <br />
                    {prop.data.status.includes("FAIL") ? (
                        <Row>
                            <Col xs={6}>
                                {prop.data.status === "CREATE_FAIL" ? (
                                    <Button variant="outlined" color="secondary" style={{ width: "100%" }} onClick={() => reCreateNetwork(prop.data.network_id)}>
                                        Recreate
                                    </Button>
                                ) : prop.data.status === "UPDATE_FAIL" ? (
                                    <ButtonGroup variant="outlined" color="secondary" style={{ width: "100%" }}>
                                        <Button onClick={() => reUpdateNetwork(prop.data.network_id)}>Re-Update</Button>
                                        <Button onClick={() => rollbacknetwork(prop.data.network_id)}>Rollback</Button>
                                    </ButtonGroup>
                                ) : (
                                    <Button variant="outlined" color="secondary" style={{ width: "100%" }} onClick={() => deletenetwork(prop.data.network_id)}>
                                        Re-Delete
                                    </Button>
                                )}
                            </Col>
                            <Col xs={6} style={{ textAlign: "right" }}>
                                <Button variant="contained" color="secondary" style={{ width: "100%" }} onClick={() => deletenetwork(prop.data.network_id)}>
                                    Terminate
                                </Button>
                            </Col>
                        </Row>
                    ) : (
                        <Row>
                            <Col xs={6}>
                                <Button
                                    disabled={prop.data.status.includes("PENDING")}
                                    variant="outlined"
                                    color="primary"
                                    style={{ width: "100%" }}
                                    onClick={() => {
                                        dispatch({ type: VIEW_MORE, payload: prop.data });
                                        navigate(`${prop.data.network_id}`);
                                    }}
                                >
                                    {"Detail"}
                                </Button>
                            </Col>
                            <Col xs={6} style={{ textAlign: "right" }}>
                                <Button disabled={prop.data.status.includes("PENDING")} onClick={() => handleExplorer()} color="primary" variant="contained" style={{ width: "100%" }}>
                                    {"Explorer"}
                                </Button>
                            </Col>
                        </Row>
                    )}
                </CardBody>
            </Card>
        </Col>
    );
};

export default CardNetwork;
