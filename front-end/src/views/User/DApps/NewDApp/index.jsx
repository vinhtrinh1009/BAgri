import React, { useState } from "react";
import { Container, Row, Col, Card, CardBody } from "reactstrap";
import Step1 from "./components/step1/Step1";
import Step2 from "./components/step2/Step2";
import Step3 from "./components/step3/Step3";
import { Stepper, Step, StepLabel } from "@mui/material";

const NewDApp = () => {
    const [activeStep, setActiveStep] = useState(0);
    function jumpToStep(number) {
        setActiveStep(number);
    }
    const steps = [
        { name: "Application Config", component: <Step1 jumpToStep={jumpToStep} /> },
        { name: "Business Config", component: <Step2 jumpToStep={jumpToStep} /> },
        { name: "Review Config", component: <Step3 jumpToStep={jumpToStep} /> },
    ];

    return (
        <>
            {activeStep !== 1 ? (
                <>
                    <Container style={{ maxWidth: "1605px", margin: "0 auto" }}>
                        <Row>
                            <Col sm={4}>
                                <strong style={{ font: "normal normal bold 24px/28px Roboto", margin: "40px 0px 36px 0px" }}>New DApp</strong>
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
                                <Card style={{ boxShadow: "0px 3px 12px #0000001F", minHeight: "583px" }}>
                                    <CardBody style={{ padding: "80px 30px 110px 30px" }}>{steps[activeStep].component}</CardBody>
                                </Card>
                            </Col>
                        </Row>
                    </Container>
                </>
            ) : (
                <div style={{ margin: "0 -15px 0px -15px" }}>{steps[activeStep].component}</div>
            )}
        </>
    );
};

export default NewDApp;
