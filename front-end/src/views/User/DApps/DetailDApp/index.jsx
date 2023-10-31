import { Button } from "@material-ui/core";
import axios from "axios";
import React, { Fragment, useEffect, useState } from "react";
import { RotateCcw, Edit3, Trash2 } from "react-feather";
import ReactFlow, { Background, Controls, MiniMap } from "react-flow-renderer";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router";
import { Container, Row, Col, Card, CardBody, Media } from "reactstrap";
import logo from "src/assets/images/dapp.png";
import { Link } from "react-router-dom";
import errorImg from "src/assets/images/search-not-found.png";
import { CORE_SERVICE_URL } from "src/constant/config";
import { STEP2_RELATIONSHIPS } from "src/redux/User/DApps/actionTypes";
import { getToken } from "src/utils/token";
import { networkStatus } from "../../../../constant/networkStatus";
import { statusNetworkClassName } from "../../../../constant/statusNetworkClassName";
import { OPEN_ERROR_ALERT } from "../../../../redux/User/Alerts/actionTypes";
import { OPEN_SUCCESS_ALERT } from "../../../../redux/User/Alerts/actionTypes";
import { retryCreateDapp, retryUpdateDapp, rollBackDapp, deleteDApps } from "../../../../services/User/dapps";

import CustomNodeFlow from "../NewDApp/components/custom_react_flow/CustomNodeFlow";
import FloatingEdge from "../NewDApp/components/custom_react_flow/FloatingEdge";

export default function DetailDApp() {
    let { dappId } = useParams();
    const dispatch = useDispatch();
    const [dapp, setDapp] = useState();
    const layout = useSelector((state) => state.Storage.layout);
    const userData = useSelector((stores) => stores.User.user);
    let temp = null;
    let entities = [];
    let relationships = [];

    async function getDAppById(params) {
        const response = await axios({
            method: "GET",
            url: `${CORE_SERVICE_URL}/dapps/${params}`,
            headers: {
                "Content-Type": "application/json",
                Authorization: getToken(),
            },
            timeout: 30000,
        });
        setDapp(response.data.data[0]);
        return response;
    }

    async function reCreateDapp() {
        const res = await retryCreateDapp(dappId);
        if (res.status === "success") {
            dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Send request done!" } });
        } else {
            dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Send request fail!" } });
        }
    }
    async function reUpdateDapp() {
        const res = await retryUpdateDapp(dappId);
        if (res.status === "success") {
            dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Send request done!" } });
        } else {
            dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Send request fail!" } });
        }
    }

    async function rollbackDapp() {
        const res = await rollBackDapp(dappId);
        if (res.status === "success") {
            dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Send request done!" } });
            setTimeout(() => {
                window.location.href = "/dapps";
            }, 700);
        } else {
            dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Send request fail!" } });
        }
    }

    async function deleteDapp() {
        const res = await deleteDApps(dappId);
        if (res.status === "success") {
            dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Delete done!" } });
            setTimeout(() => {
                window.location.href = "/dapps";
            }, 700);
        } else {
            dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Have error happened, action fail!" } });
        }
    }

    useEffect(() => {
        getDAppById(dappId);
    }, []);

    useEffect(() => {
        if (dapp && dapp.message) {
            dispatch({ type: OPEN_ERROR_ALERT, payload: { message: dapp.message } })
        }
    }, [dapp])

    if (dapp && dapp.entities) {
        dapp.entities.map((value, key) => {
            temp = {
                id: value.name,
                type: "customNode",
                data: value,
                position: { x: 50 + key * 300, y: 50 + (key - 1) * 50 },
            };
            entities.push(temp);
            value &&
                value.relationships &&
                value.relationships.map((edge, id) => {
                    temp = {
                        source: value.name,
                        sourceHandle: null,
                        target: edge.reference_to_entity,
                        targetHandle: null,
                        id: value.name + "-" + edge.type + "-" + edge.reference_to_entity,
                        data: {
                            id: value.name + "-" + edge.type + "-" + edge.reference_to_entity,
                            source: value.name,
                            target: edge.reference_to_entity,
                            type: edge.type,
                        },
                        type: "customEdge",
                    };
                    relationships.push(temp);
                });
        });
        dispatch({ type: STEP2_RELATIONSHIPS, payload: relationships });
    }
    const nodeTypes = {
        customNode: CustomNodeFlow,
    };
    const edgeTypes = {
        customEdge: FloatingEdge,
    };
    const onLoad = (reactFlowInstance) => reactFlowInstance.fitView();

    return dapp ? (
        <Fragment>
            <Container style={{ maxWidth: "1605px", margin: "0 auto" }}>
                <div style={{ padding: "30px 0px" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
                        <h5 style={{ display: "flex", alignItems: "center" }}>
                            <div className="avatars mr-3">
                                <div className="avatar">
                                    <Media
                                        body
                                        className="img-60 rounded-circle"
                                        src={dapp.dapp_logo || logo}
                                        alt="#"
                                        onError={(e) => {
                                            e.currentTarget.src = logo;
                                        }}
                                    />
                                </div>
                            </div>
                            <div style={{ textTransform: "capitalize" }}>
                                {dapp.dapp_name && dapp.dapp_name}
                                <div className="state">
                                    <div className={`dot-notify ${statusNetworkClassName[dapp.status] || statusNetworkClassName.ELSE}`}></div>
                                    <div style={{ opacity: "0.5" }}>{networkStatus[dapp.status] || networkStatus.ELSE}</div>
                                </div>
                            </div>
                        </h5>
                        {dapp.status === "CREATE_FAIL" ? (
                            <div className="media-body text-right">
                                <Button onClick={reCreateDapp} className="mr-2" color="secondary" variant="outlined" style={{ textTransform: "none" }}>
                                    <RotateCcw className="mr-2" width={19} height={19} />
                                    {"Retry"}
                                </Button>
                                <Button onClick={deleteDapp} className="" color="secondary" variant="contained" style={{ textTransform: "none" }}>
                                    <Trash2 className="mr-2" width={19} height={19} />
                                    {"Delete"}
                                </Button>
                            </div>
                        ) : dapp.status === "UPDATE_FAIL" ? (
                            <div className="media-body text-right">
                                <Button onClick={rollbackDapp} className="mr-2" color="secondary" variant="text" style={{ textTransform: "none" }}>
                                    {/* <RotateCcw className="mr-2" width={19} height={19} /> */}
                                    {"Rollback"}
                                </Button>
                                <Button onClick={reUpdateDapp} className="mr-2" color="secondary" variant="outlined" style={{ textTransform: "none" }}>
                                    <RotateCcw className="mr-2" width={19} height={19} />
                                    {"Retry"}
                                </Button>
                                <Button onClick={deleteDapp} className="" color="secondary" variant="contained" style={{ textTransform: "none" }}>
                                    <Trash2 className="mr-2" width={19} height={19} />
                                    {"Delete"}
                                </Button>
                            </div>
                        ) : (
                            <div className="media-body text-right">
                                <Link to={`/dapps/edit/${dappId}`}>
                                    <Button disabled={dapp.status.includes("PENDING")} className="mr-2" color="primary" variant="outlined" style={{ textTransform: "none" }}>
                                        <Edit3 className="mr-2" width={19} height={19} />
                                        {"Edit"}
                                    </Button>
                                </Link>
                                <Button disabled={dapp.status.includes("PENDING")} onClick={deleteDapp} className="" color="primary" variant="contained" style={{ textTransform: "none" }}>
                                    <Trash2 className="mr-2" width={19} height={19} />
                                    {"Delete"}
                                </Button>
                            </div>
                        )}
                    </div>
                    <Card>
                        <CardBody style={{ padding: "30px" }}>
                            <h6 style={{ color: "#8CB8D8" }}>BASIC INFORMATION</h6>
                            <br />
                            <Row>
                                <Col className="col-md-4">
                                    <div className="mb-1" style={{ opacity: "0.65" }}>
                                        Name
                                    </div>
                                    <strong>{dapp.dapp_name}</strong>
                                </Col>
                                <Col className="col-md-4">
                                    <div className="mb-1" style={{ opacity: "0.65" }}>
                                        Description
                                    </div>
                                    <strong>{dapp.dapp_description}</strong>
                                </Col>
                                <Col className="col-md-4">
                                    <div className="mb-1" style={{ opacity: "0.65" }}>
                                        Status
                                    </div>
                                    <strong>
                                        {networkStatus[dapp.status] || networkStatus.ELSE}
                                    </strong>
                                </Col>
                            </Row>
                            <br />
                            <Row>
                                <Col className="col-md-4">
                                    <div className="mb-1" style={{ opacity: "0.65" }}>
                                        DApp ID
                                    </div>
                                    <strong>{dapp.dapp_id}</strong>
                                </Col>
                                <Col className="col-md-4">
                                    <div className="mb-1" style={{ opacity: "0.65" }}>
                                        Network ID
                                    </div>
                                    <strong>{dapp.network_id}</strong>
                                </Col>
                                <Col className="col-md-4">
                                    <div className="mb-1" style={{ opacity: "0.65" }}>
                                        Owner
                                    </div>
                                    <strong>{userData.full_name}</strong>
                                </Col>
                            </Row>

                            <br />
                            <br />
                            <hr />
                            <br />
                            <h6 style={{ color: "#8CB8D8" }}>ENTITIES INFORMATION</h6>
                            <br />
                            <br />
                            <Row>
                                <ReactFlow
                                    minZoom={1}
                                    maxZoom={1}
                                    style={{ width: "100%", height: "40rem", zIndex: "0" }}
                                    elements={[...dapp.diagrams, ...relationships]}
                                    nodeTypes={nodeTypes}
                                    edgeTypes={edgeTypes}
                                    onlyRenderVisibleElements={false}
                                    onLoad={onLoad}
                                    snapToGrid={true}
                                    snapGrid={[15, 15]}
                                    key="edges"
                                    nodesConnectable={false}
                                    nodesDraggable={false}
                                    elementsSelectable={false}
                                >
                                    <MiniMap
                                        nodeColor={(node) => {
                                            return node.data.color;
                                        }}
                                    />
                                    <Controls />
                                    <Background variant="dots" color="#f1f6f8" style={layout === "light" || layout === "" ? { backgroundColor: "#f1f6f8" } : ""} />
                                </ReactFlow>
                            </Row>
                        </CardBody>
                    </Card>
                </div>
            </Container>
        </Fragment>
    ) : (
        <>
            <img className="img-fluid m-auto" src={errorImg} alt="" style={{ display: "flex" }} />
        </>
    );
}
