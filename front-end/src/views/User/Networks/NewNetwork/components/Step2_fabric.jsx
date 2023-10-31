import NodePlan from "./NodePlan";
import React, { useState, useEffect } from "react";
import { Row, Col } from "reactstrap";
import { NODE_PLAN, NUMBER_NODES } from "../../../../../redux/User/Networks/actionTypes";
import { useDispatch, useSelector } from "react-redux";
import Organization from "./Organization";
import { ADD_ORGANIZATIONS } from "src/redux/User/Networks/actionTypes";
import InputNumber from "./InputNumber";
import { isPositiveNumber } from "src/utils/stringhandle";
import { Button } from "@mui/material";
import { v4 as uuidv4 } from "uuid";

const Step2_fabric = (props) => {
    const dispatch = useDispatch();
    const numberNodes = useSelector((state) => state.Network.numberNodes);
    const nodePlan = useSelector((state) => state.Network.nodePlan);
    const organizations = useSelector((state) => state.Network.organizations);

    const handleChangeNumberNodes = (event) => {
        dispatch({ type: NUMBER_NODES, payload: event.target.value });
    };
    const selected = (value, key) => {
        dispatch({ type: NODE_PLAN, payload: value });
    };
    const [keyOrg, setKeyOrg] = useState(uuidv4());
    const checkOrganizations = () => {
        const length = organizations.length;
        for (let i = 0; i < length; i++) {
            if (organizations[i].name === "") return false;
            if (isPositiveNumber(organizations[i].number_peer) == false) return false;
            for (let j = i + 1; j < length; j++) {
                if (organizations[j].name === "") return false;
                if (organizations[i].name === organizations[j].name) return false;
            }
        }
        return true;
    };
    useEffect(() => {
        setKeyOrg(uuidv4());
    }, [organizations.length]);
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
                </Row>

                {organizations.map((value, index) => {
                    return <Organization key={keyOrg + "fabric" + index} index={index} />;
                })}
                <Row>
                    <Col md={8}></Col>
                    <Col md={4}>
                        <Button
                            style={{ fontSize: "14px", width: "100%", background: "#ecf6fe", textTransform: "unset" }}
                            className="insert-btn"
                            variant="text"
                            onClick={() => {
                                dispatch({ type: ADD_ORGANIZATIONS, payload: { name: "", number_peer: "" } });
                            }}
                        >
                            Add new organization
                        </Button>
                    </Col>
                </Row>
            </div>

            <br />
            <div className={""}>
                <h5 className="mb-3" style={{ color: "#8CB8D8" }}>
                    NODE PLAN
                </h5>
                <div className="flex_box_row">
                    {NodePlan.map((value, key) => (
                        <div className="flex_box_col" key={value.cpu + "fabric" + key} onClick={() => selected(value, key)}>
                            <div className={key === nodePlan?.id ? "card node-plan node-plan-active" : "card node-plan"}>
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
                        disabled={!(isPositiveNumber(numberNodes) && checkOrganizations() && nodePlan)}
                        style={{ width: "109px", height: "36px" }}
                    >
                        {"Next"}
                    </Button>
                </Col>
            </Row>
        </div>
    );
};

export default Step2_fabric;
