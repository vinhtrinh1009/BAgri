import NodePlan from "./NodePlan";
import React from "react";
import { Row, Col } from "reactstrap";
import { NODE_PLAN, NUMBER_NODES, NUMBER_OF_PEERS } from "../../../../../redux/User/Networks/actionTypes";
import { useDispatch, useSelector } from "react-redux";
import { Button } from "@mui/material";
import InputNumber from "./InputNumber";
import { isPositiveNumber } from "src/utils/stringhandle";

const Step2_sawtooth = (props) => {
    const dispatch = useDispatch();
    const numberNodes = useSelector((state) => state.Network.numberNodes);
    const numberOfPeers = useSelector((state) => state.Network.numberOfPeers);
    const nodePlan = useSelector((state) => state.Network.nodePlan);

    const handleChangeNumberNodes = (event) => {
        dispatch({ type: NUMBER_NODES, payload: event.target.value });
    };
    const handleChangeNumberOfPeers = (event) => {
        dispatch({ type: NUMBER_OF_PEERS, payload: event.target.value });
    };

    const selected = (value, key) => {
        dispatch({ type: NODE_PLAN, payload: value });
    };

    return (
        <div>
            <div className="input-f">
                <Row className="form-row">
                    <Col md="12 mb-3">
                        <InputNumber
                            label="Number Nodes"
                            variant="filled"
                            OnChange={handleChangeNumberNodes}
                            value={numberNodes}
                            onlyPositive={true}
                            required={true}
                            style={{ marginBottom: "31px" }}
                        />
                    </Col>
                    <Col md="12 mb-3">
                        <InputNumber label="Number Peers" variant="filled" OnChange={handleChangeNumberOfPeers} value={numberOfPeers} onlyPositive={true} required={true} />
                    </Col>
                </Row>
            </div>

            <br />
            <div>
                <h5 className="mb-3" style={{ color: "#8CB8D8" }}>
                    Node Plan
                </h5>
                <div className="flex_box_row">
                    {NodePlan.map((value, key) => (
                        <div className="flex_box_col" key={value.cpu + "sawtooth" + key} onClick={() => selected(value, key)}>
                            <div className={key === nodePlan?.id ? "node-plan node-plan-active card" : "node-plan card"}>
                                <b style={{ fontSize: "20px", marginBottom: "18px" }}>{value.name}</b>
                                <span style={{ opacity: "0.65", fontSize: "16px" }}>{value.ram}GB RAM </span>
                                <span style={{ opacity: "0.65", fontSize: "16px" }}>{value.cpu} vCPUs</span>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
            <Row style={{ marginTop: "30px" }}>
                <Col xs={6} style={{ textAlign: "right" }}>
                    <Button color="primary" variant="outlined" onClick={() => props.jumpToStep(0)} style={{ width: "109px", height: "36px" }}>
                        {"Back"}
                    </Button>
                </Col>
                <Col xs={6} style={{ textAlign: "left" }}>
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={() => props.jumpToStep(2)}
                        disabled={!(isPositiveNumber(numberNodes) && isPositiveNumber(numberOfPeers) && nodePlan)}
                        style={{ width: "109px", height: "36px" }}
                    >
                        {"Next"}
                    </Button>
                </Col>
            </Row>
        </div>
    );
};

export default Step2_sawtooth;
