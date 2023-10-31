import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import StepZilla from "react-stepzilla";
import { Stepper, Step, StepLabel } from "@mui/material";
import { Container, Row, Col, Card, CardHeader, CardBody } from "reactstrap";
import Step0 from "./components/Step0";
import Step1 from "./components/Step1";
import Step2 from "./components/Step2";
import Step3 from "./components/Step3";

const NewToken = () => {
    const [activeStep, setActiveStep] = useState(0);
    const [data, setData] = useState(undefined);
    const handleUpdateData = (newData) => {
        setData(newData);
    };

    function jumpToStep(number) {
        setActiveStep(number);
    }

    const steps = [
        { name: "Network", component: <Step0 data={data} onDataChange={handleUpdateData} jumpToStep={jumpToStep} /> },
        { name: "Basic Information", component: <Step1 data={data} onDataChange={handleUpdateData} jumpToStep={jumpToStep} /> },
        { name: "Deploy", component: <Step2 data={data} onDataChange={handleUpdateData} jumpToStep={jumpToStep} /> },
        { name: "Finish", component: <Step3 data={data} onDataChange={handleUpdateData} jumpToStep={jumpToStep} /> },
    ];

    return (
        <>
            <Container style={{ maxWidth: "1605px", margin: "0px auto", paddingTop: "30px" }}>
                <Row>
                    <Col sm={4} style={{ display: "flex", alignItems: "center", justifyContent: "left" }}>
                        <strong style={{ font: "normal normal bold 24px/28px Roboto" }}>New Token</strong>
                    </Col>
                    <Col sm={8} style={{ display: "flex", alignItems: "center", justifyContent: "right" }}>
                        <div style={{ width: "100%", maxWidth: "648px" }}>
                            <Stepper activeStep={activeStep}>
                                {steps.map((step, index) => {
                                    return (
                                        <Step key={step.name} className={index === activeStep ? "active_step" : ""}>
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
                        <Card style={{ minHeight: "583px", marginTop: "2%" }}>
                            <CardBody style={{ padding: "80px 30px 110px 30px" }}>{steps[activeStep].component}</CardBody>
                        </Card>
                    </Col>
                </Row>
            </Container>
        </>
    );
};

export default NewToken;
