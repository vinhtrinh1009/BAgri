import React, { Fragment, useState } from "react";
import { useSelector } from "react-redux";
import { Container, Row, Col, Card, CardBody } from "reactstrap";
import Step1 from "./components/Step1";
import Step2_sawtooth from "./components/Step2_sawtooth";
import Step2_fabric from "./components/Step2_fabric";
import Step3 from "./components/Step3";
import { Stepper, Step, StepLabel } from "@mui/material";

const NewNetwork = () => {
    const engineBlockchain = useSelector((state) => state.Network.engineBlockchain);
    const [activeStep, setActiveStep] = useState(0);
    function jumpToStep(number) {
        setActiveStep(number);
    }
    const steps = [
        {
            name: "Blockchain Config",
            component: <Step1 jumpToStep={jumpToStep} />,
        },
        {
            name: "Cluster Config",
            component: engineBlockchain === "Hyperledger Sawtooth" ? <Step2_sawtooth jumpToStep={jumpToStep} /> : <Step2_fabric jumpToStep={jumpToStep} />,
        },
        {
            name: "Review Config",
            component: <Step3 jumpToStep={jumpToStep} />,
        },
    ];
    return (
        <Fragment>
            <Container style={{ maxWidth: "1605px", margin: "0 auto" }}>
                <Row>
                    <Col sm={4}>
                        <strong style={{ font: "normal normal bold 24px/28px Roboto", margin: "40px 0px 36px 0px" }}>New Network</strong>
                    </Col>
                    <Col sm={8} style={{ display: "flex", alignItems: "center", justifyContent: "right" }}>
                        <div style={{ width: "100%", maxWidth: "648px" }}>
                            <Stepper activeStep={activeStep}>
                                {steps.map((step, index) => {
                                    return (
                                        <Step key={step.name} className={index == activeStep ? "active_step" : ""}>
                                            <StepLabel>{step.name}</StepLabel>
                                        </Step>
                                    );
                                })}
                            </Stepper>
                        </div>
                    </Col>
                </Row>
                <Row>
                    <Col sm="12">
                        <Card style={{ boxShadow: "0px 3px 12px #0000001F" }}>
                            <CardBody style={{ padding: "80px 30px 110px 30px" }}>{steps[activeStep].component}</CardBody>
                        </Card>
                    </Col>
                </Row>
            </Container>
        </Fragment>
    );
};

export default NewNetwork;
