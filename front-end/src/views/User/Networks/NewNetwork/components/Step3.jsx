import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { Col, Row } from "reactstrap";
import { UPDATE_ORGANIZATIONS } from "src/redux/User/Networks/actionTypes";
import { NODE_PLAN } from "src/redux/User/Networks/actionTypes";
import { NUMBER_NODES } from "src/redux/User/Networks/actionTypes";
import { NUMBER_OF_PEERS } from "src/redux/User/Networks/actionTypes";
import { CLUSTER_NAME } from "src/redux/User/Networks/actionTypes";
import { CONSENSUS } from "src/redux/User/Networks/actionTypes";
import { ENGINE_BLOCKCHAIN } from "src/redux/User/Networks/actionTypes";
import { createNetwork } from "src/services/User/networks";
import { Button } from "@mui/material";

export default function Step3(props) {
    const engineBlockchain = useSelector((state) => state.Network.engineBlockchain);
    const consensus = useSelector((state) => state.Network.consensus);
    const clusterName = useSelector((state) => state.Network.clusterName);
    const numberNodes = useSelector((state) => state.Network.numberNodes);
    const numberOfPeers = useSelector((state) => state.Network.numberOfPeers);
    const organizations = useSelector((state) => state.Network.organizations);
    const nodePlan = useSelector((state) => state.Network.nodePlan);
    const dispatch = useDispatch();
    const clear = () => {
        dispatch({ type: ENGINE_BLOCKCHAIN, payload: "" });
        dispatch({ type: CONSENSUS, payload: "" });
        dispatch({ type: NUMBER_NODES, payload: "" });
        dispatch({ type: NUMBER_OF_PEERS, payload: "" });
        dispatch({ type: CLUSTER_NAME, payload: "" });
        dispatch({ type: NODE_PLAN, payload: "" });
        dispatch({ type: UPDATE_ORGANIZATIONS, payload: [{ name: "", number_peer: "" }] });
    };

    const submitFun = () => {
        alert("successfully updated");
        window.location.reload();
    };
    const handleSubmit = async () => {
        if (engineBlockchain === "Hyperledger Fabric") {
            const newFabric = {
                name: clusterName,
                blockchain_type: "fabric",
                consensus: consensus.toLowerCase(),
                node_infrastructure: {
                    type: "internal",
                    number_vm_nodes: numberNodes,
                    node_plan: {
                        cpu: nodePlan.cpu,
                        ram: nodePlan.ram,
                        disk: nodePlan.storage,
                    },
                },
                blockchain_peer_config: {
                    organizations: organizations,
                },
            };
            await createNetwork(newFabric);
            window.location.href = "/networks";
            clear();
        } else {
            const newSawtooth = {
                name: clusterName,
                blockchain_type: "sawtooth",
                consensus: consensus.toLowerCase(),
                node_infrastructure: {
                    type: "internal",
                    number_vm_nodes: numberNodes,
                    node_plan: {
                        cpu: nodePlan.cpu,
                        ram: nodePlan.ram,
                        disk: nodePlan.storage,
                    },
                },
                blockchain_peer_config: {
                    number_peer: Number(numberOfPeers),
                },
            };
            await createNetwork(newSawtooth);
            window.location.href = "/networks";
            clear();
        }
    };
    return (
        <div className="step_3">
            <Row className="setup_info">
                <Col md={6}>
                    <span>Blockchain engine:</span>
                </Col>
                <Col md={6}>
                    <span>{engineBlockchain}</span>
                </Col>
            </Row>
            <Row className="setup_info">
                <Col md={6}>
                    <span>Consensus:</span>
                </Col>
                <Col md={6}>
                    <span>{consensus}</span>
                </Col>
            </Row>
            <Row className="setup_info">
                <Col md={6}>
                    <span>Cluster Name:</span>
                </Col>
                <Col md={6}>
                    <span>{clusterName}</span>
                </Col>
            </Row>
            <Row className="setup_info">
                <Col md={6}>
                    <span>Number Nodes:</span>
                </Col>
                <Col md={6}>
                    <span>{numberNodes}</span>
                </Col>
            </Row>
            <Row className="setup_info">
                <Col md={6}>
                    <span>Node Plan:</span>
                </Col>
                <Col md={6}>
                    <span>{nodePlan.name}</span>
                </Col>
            </Row>
            {engineBlockchain === "Hyperledger Sawtooth" ? (
                <Row className="setup_info">
                    <Col md={6}>
                        <span>Number Of Peers:</span>{" "}
                    </Col>
                    <Col md={6}>
                        <span>{numberOfPeers}</span>
                    </Col>
                </Row>
            ) : (
                organizations.map((value, key) => (
                    <Row key={"organzationstep3" + key} className="setup_info">
                        <Col md={6}>
                            <span> Organization {key + 1}: </span>
                        </Col>
                        <Col md={6}>
                            {value.name} - {value.number_peer} peers
                        </Col>
                    </Row>
                ))
            )}

            <Row style={{ marginTop: "32px" }}>
                <Col xs={6} style={{ textAlign: "right" }}>
                    <Button color="primary" variant="outlined" onClick={() => props.jumpToStep(1)} style={{ width: "109px", height: "36px" }}>
                        {"Back"}
                    </Button>
                </Col>
                <Col xs={6} style={{ textAlign: "left" }}>
                    <Button variant="contained" color="primary" onClick={handleSubmit} style={{ width: "109px", height: "36px" }}>
                        {"Submit"}
                    </Button>
                </Col>
            </Row>
            {/* <Button color="primary" className=" pull-left" onClick={() => props.jumpToStep(1)}>
                {"Back"}
            </Button>
            <Link to="/networks" className="btn btn-primary pull-right" onClick={handleSubmit}>
                {"Submit"}
            </Link> */}
        </div>
    );
}
