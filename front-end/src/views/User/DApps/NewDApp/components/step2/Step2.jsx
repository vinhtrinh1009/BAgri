import React from "react";
import Step2Sidebar from "./Step2Sidebar";
import { Row, Col } from "reactstrap";
import { Stepper, Step, StepLabel, Button } from "@mui/material";
import Step2Diagram from "./Step2Diagram";
import { useDispatch, useSelector } from "react-redux";
import { SELECTED_NODE } from "src/redux/User/DApps/actionTypes";

export default function Step2(props) {
    const steps = ["Application Config", "Business Config", "Review Config"];
    const dispatch = useDispatch();
    const step2Entities = useSelector((state) => state.DApp.step2Entities);

    function gotoStep3() {
        dispatch({ type: SELECTED_NODE, payload: "null" });
        props.jumpToStep(2);
    }
    function checkEmptyEntity() {
        if (step2Entities.length === 0) return true;
        return false;
    }
    return (
        <div className="step2_new_dapp">
            <Step2Sidebar />
            <div className="step2_content">
                <div className="step2_header" style={{ margin: "0px 0px 30px 0px" }}>
                    <Row style={{ margin: "0px" }}>
                        <Col sm={12} style={{ display: "flex", alignItems: "center", justifyContent: "right" }}>
                            <div style={{ width: "100%", maxWidth: "648px" }}>
                                <Stepper activeStep={1}>
                                    {steps.map((step, index) => {
                                        return (
                                            <Step key={step} className={index == 1 ? "active_step" : ""}>
                                                <StepLabel>{step}</StepLabel>
                                            </Step>
                                        );
                                    })}
                                </Stepper>
                            </div>
                        </Col>
                    </Row>
                </div>
                <div className="diagram">
                    <Step2Diagram />
                </div>
                <Row className="step2_footer" style={{ margin: "30px 0px 0px 0px" }}>
                    <Col xs={6} style={{ textAlign: "right" }}>
                        <Button color="primary" variant="outlined" onClick={() => props.jumpToStep(0)} style={{ width: "110px", height: "36px" }}>
                            {"Back"}
                        </Button>
                    </Col>
                    <Col xs={6} style={{ textAlign: "left" }}>
                        <Button variant="contained" color="primary" onClick={gotoStep3} disabled={checkEmptyEntity()} style={{ width: "110px", height: "36px" }}>
                            {"Next"}
                        </Button>
                    </Col>
                </Row>
            </div>
        </div>
    );
}
