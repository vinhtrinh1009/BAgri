import React, { useEffect, useState } from "react";
import { Container, Row, Col, Card, CardBody, Media } from "reactstrap";
import Step1 from "./step1/Step1";
import Step2 from "./step2/Step2";
import Step3 from "./step3/Step3";
import { Link } from "react-router-dom";
import logo from "src/assets/images/dapp.png";
import { Stepper, Step, StepLabel, Button } from "@mui/material";
import { useNavigate, useParams } from "react-router";
import { getDetailDAppById } from "../../../../services/User/dapps";
import { statusNetworkClassName } from "../../../../constant/statusNetworkClassName";
import { networkStatus } from "../../../../constant/networkStatus";
import { Navigation } from "react-feather";
import { useDispatch } from "react-redux";
import { STEP1_DATA } from "../../../../redux/User/DApps/actionTypes";
import { OPEN_ERROR_ALERT } from "../../../../redux/User/Alerts/actionTypes";
import { useSelector } from "react-redux";
import { STEP2_ENTITIES } from "../../../../redux/User/DApps/actionTypes";
import { STEP2_RELATIONSHIPS } from "../../../../redux/User/DApps/actionTypes";
import { CLEAR_DAPP_STATE } from "../../../../redux/User/DApps/actionTypes";

export default function EditDApp() {
    const { dappId } = useParams();
    const dispatch = useDispatch();
    const dapp = useSelector((stores) => stores.DApp);
    const navigate = useNavigate();

    const [activeStep, setActiveStep] = useState(0);
    function jumpToStep(number) {
        setActiveStep(number);
    }
    const steps = [
        { name: "Application Config", component: <Step1 jumpToStep={jumpToStep} /> },
        { name: "Business Config", component: <Step2 jumpToStep={jumpToStep} dappId={dappId} /> },
        { name: "Review Config", component: <Step3 jumpToStep={jumpToStep} dappId={dappId} /> },
    ];

    useEffect(() => {
        (async () => {
            const res = await getDetailDAppById(dappId);
            if (res.status == "success") {
                const dappInfo = res.data[0];
                dispatch({
                    type: STEP1_DATA,
                    payload: {
                        dapp_name: dappInfo.dapp_name,
                        dapp_description: dappInfo.dapp_description,
                        network_id: dappInfo.network_id,
                        encryption_type: dappInfo.encryption_type,
                        dapp_logo: dappInfo.dapp_logo || logo,
                        status: dappInfo.status,
                    },
                });

                const entityLength = dappInfo.entities.length;
                const diagramLength = dappInfo.diagrams.length;
                let entityList = [];
                let relationShipList = [];
                for (let i = 0; i < diagramLength; i++) {
                    if (i < entityLength) {
                        entityList.push({
                            ...dappInfo.diagrams[i],
                            data: {
                                ...dappInfo.diagrams[i].data,
                                is_old_data: true,
                                attributes: dappInfo.diagrams[i].data.attributes.map((attr, index) => {
                                    return {
                                        ...attr,
                                        is_old_data: true,
                                    };
                                }),
                            },
                        });
                    } else {
                        relationShipList.push({
                            ...dappInfo.diagrams[i],
                            data: {
                                ...dappInfo.diagrams[i].data,
                                is_old_data: true,
                            },
                        });
                    }
                }

                dispatch({ type: STEP2_ENTITIES, payload: entityList });
                dispatch({ type: STEP2_RELATIONSHIPS, payload: relationShipList });
            } else {
                dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "DApp is not exist!" } });
                setTimeout(() => {
                    navigate(`/dapps`);
                }, 700);
            }
        })();

        return () => {
            dispatch({ type: CLEAR_DAPP_STATE });
        };
    }, []);

    return (
        <>
            {activeStep !== 1 ? (
                <>
                    <Container style={{ maxWidth: "1605px", margin: "0px auto", paddingTop: "30px" }}>
                        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
                            <h5 style={{ display: "flex", alignItems: "center" }}>
                                <div className="avatars mr-3">
                                    <div className="avatar">
                                        <Media
                                            body
                                            className="img-60 rounded-circle"
                                            src={dapp.step1Data.dapp_logo}
                                            alt="#"
                                            onError={(e) => {
                                                e.currentTarget.src = logo;
                                            }}
                                        />
                                    </div>
                                </div>
                                <div style={{ textTransform: "capitalize" }}>
                                    {dapp.step1Data?.dapp_name || "No Name App"}
                                    <div className="state">
                                        <div className={`dot-notify ${statusNetworkClassName[dapp.step1Data.status] || statusNetworkClassName.ELSE}`}></div>
                                        <div style={{ opacity: "0.5" }}>{networkStatus[dapp.step1Data.status] || networkStatus.ELSE}</div>
                                    </div>
                                </div>
                            </h5>
                            <div className="media-body text-right">
                                <Link to={`/dapps/${dappId}`}>
                                    <Button className="mr-2" color="primary" variant="contained" style={{ textTransform: "none" }}>
                                        <Navigation className="mr-2" width={19} height={19} />
                                        {"Exit"}
                                    </Button>
                                </Link>
                            </div>
                        </div>
                        <Row>
                            <Col sm={4}>
                                <strong style={{ font: "normal normal bold 24px/28px Roboto", margin: "10px 0px 36px 0px" }}>Edit DApp</strong>
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
}
