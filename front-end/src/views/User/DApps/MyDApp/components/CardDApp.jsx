import React from "react";
import { useDispatch } from "react-redux";
import logo from "src/assets/images/dapp.png";
import { Row, Col, Card, CardBody } from "reactstrap";

import { Download, RotateCcw } from "react-feather";
import { CURRENT_DAPP } from "src/redux/User/DApps/actionTypes";
import { DOCS_DAPP_URL } from "src/constant/config";

import { Button } from "@material-ui/core";
import { useNavigate } from "react-router";
import { storageService } from "../../../../../services/User/storages";
import { OPEN_SUCCESS_ALERT } from "../../../../../redux/User/Alerts/actionTypes";
import { OPEN_ERROR_ALERT } from "../../../../../redux/User/Alerts/actionTypes";
import { OPEN_WARNING_ALERT } from "../../../../../redux/User/Alerts/actionTypes";
import FileSaver from "file-saver";
import { statusNetworkClassName } from "../../../../../constant/statusNetworkClassName";
import { networkStatus } from "../../../../../constant/networkStatus";
import { retryCreateDapp } from "../../../../../services/User/dapps";
import { retryUpdateDapp } from "../../../../../services/User/dapps";
import { retryDeleteDapp } from "../../../../../services/User/dapps";
import { rollBackDapp } from "../../../../../services/User/dapps";
import { deleteDApps } from "../../../../../services/User/dapps";
import { touchRippleClasses } from "@mui/material";

const CardDApp = (prop) => {
    const dispatch = useDispatch();
    const navigate = useNavigate();

    async function handleDownloadSDK() {
        if (prop.data.sdk_folder_id && prop.data.status !== "CREATE_PENDING") {
            const res = await storageService.downloadFolder(prop.data.sdk_folder_id);
            if (res.status === 200) {
                var blob = new Blob([res.data], { type: "application/octet-stream" });
                FileSaver.saveAs(blob, `${prop.data.dapp_name + "_sdk"}.zip`);
                setTimeout(() => {
                    dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Download done!" } });
                }, 600);
            } else {
                dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Have an error occurred! Action fail!" } });
            }
        } else {
            dispatch({ type: OPEN_WARNING_ALERT, payload: { message: "State is not ready. Cannot download SDK !" } });
        }
    }
    async function reCreateDapp(dappId) {
        const res = await retryCreateDapp(dappId);
        if (res.status !== 400) {
            dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Send request done!" } });
        } else {
            dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Send request fail!" } });
        }
    }
    async function reUpdateDapp(dappId) {
        const res = await retryUpdateDapp(dappId);
        if (res.status != 400) {
            dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Send request done!" } });
        } else {
            dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Send request fail!" } });
        }
    }
    async function reDeleteDapp(dappId) {
        const res = await retryDeleteDapp(dappId);
        if (res.status != 400) {
            dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Send request done!" } });
        } else {
            dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Send request fail!" } });
        }
    }
    async function rollbackDapp(dappId) {
        const res = await rollBackDapp(dappId);
        if (res.status != 400) {
            dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Send request done!" } });
        } else {
            dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Send request fail!" } });
        }
    }
    async function deleteDapp(dappId) {
        const res = await deleteDApps(dappId);
        if (res.status != 400) {
            dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Send request done!" } });
        } else {
            dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Send request fail!" } });
        }
    }
    return (
        <Col xl={4} md={6}>
            <Card style={{ boxShadow: "0px 3px 10px #00000019" }}>
                <CardBody style={{ border: "none", padding: "18px 24px" }}>
                    <Row>
                        <Col xs={5}>
                            <img
                                className="img-50"
                                src={prop.data.dapp_logo || logo}
                                onError={(e) => {
                                    e.currentTarget.src = logo;
                                }}
                            />
                        </Col>

                        <Col xs={7} className="text-right">
                            <div
                                style={{
                                    textTransform: "capitalize",
                                    font: "normal normal bold 20px/24px Roboto",
                                    fontWeight: "bold",
                                    overflow: "hidden",
                                    textOverflow: "ellipsis",
                                    marginBottom: "8px",
                                    whiteSpace: "nowrap",
                                }}
                            >
                                {prop.data.dapp_name}
                            </div>
                            <div className="state" style={{ justifyContent: "right" }}>
                                <div className={`dot-notify ${statusNetworkClassName[prop.data.status] || statusNetworkClassName.ELSE}`}></div>
                                <div>{networkStatus[prop.data.status] || networkStatus.ELSE}</div>
                            </div>
                        </Col>
                    </Row>
                    <br />
                    <div className="nameDApp" style={{ opacity: "0.65", height: "52px", marginBottom: "14px" }}>
                        {prop.data.dapp_description}
                    </div>

                    {prop.data.status.includes("FAIL") ? (
                        <Row>
                            <Col xs={4}>
                                {prop.data.status === "UPDATE_FAIL" ? (
                                    <Button variant="text" color="secondary" style={{ width: "100%", maxWidth: "110px" }} onClick={() => reUpdateDapp(prop.data.dapp_id)}>
                                        <RotateCcw width={24} height={24} />
                                        <span style={{ marginLeft: "5px" }}>Retry</span>
                                    </Button>
                                ) : prop.data.status === "CREATE_FAIL" ? (
                                    <Button variant="text" color="secondary" style={{ width: "100%", maxWidth: "110px" }} onClick={() => reCreateDapp(prop.data.dapp_id)}>
                                        <RotateCcw width={24} height={24} />
                                        <span style={{ marginLeft: "5px" }}>Retry</span>
                                    </Button>
                                ) : null}
                            </Col>
                            <Col xs={8} style={{ justifyContent: "right", display: "flex" }}>
                                <Button variant="outlined" color="secondary" style={{ width: "100%", maxWidth: "110px", marginRight: "10px" }} 
                                    onClick={() => {
                                        dispatch({ type: CURRENT_DAPP, payload: prop.data });
                                        navigate(`${prop.data.dapp_id}`);
                                    }}>
                                    Detail
                                </Button>
                                <Button variant="contained" color="secondary" style={{ width: "100%", maxWidth: "110px" }} onClick={() => deleteDapp(prop.data.dapp_id)}>
                                    Delete
                                </Button>
                            </Col>
                        </Row>
                    ) : (
                        <Row>
                            <Col xs={4}>
                                <Button disabled={prop.data.status.includes("PENDING")} onClick={() => handleDownloadSDK()} variant="text" color="primary" style={{ width: "100%", maxWidth: "110px" }}>
                                    <Download width={24} height={24} />
                                    <span style={{ marginLeft: "5px" }}>SDK</span>
                                </Button>
                            </Col>
                            <Col xs={8} style={{ justifyContent: "right", display: "flex" }}>
                                <Button
                                    // disabled={prop.data.status.includes("PENDING")}
                                    variant="outlined"
                                    color="primary"
                                    style={{ width: "100%", maxWidth: "110px", marginRight: "10px" }}
                                    onClick={() => {
                                        dispatch({ type: CURRENT_DAPP, payload: prop.data });
                                        navigate(`${prop.data.dapp_id}`);
                                    }}
                                >
                                    {"Detail"}
                                </Button>

                                <Button
                                    disabled={prop.data.status.includes("PENDING")}
                                    variant="contained"
                                    color="primary"
                                    style={{ width: "100%", maxWidth: "110px" }}
                                    onClick={() => window.open(`${DOCS_DAPP_URL}/${prop.data.dapp_id}/index.html`, "_blank")}
                                >
                                    {"Docs"}
                                </Button>
                            </Col>
                        </Row>
                    )}

                    {/* {prop.data.status.includes("FAIL") ? (
                        <Row>
                            <Col xs={4}>
                                {prop.data.status === "UPDATE_FAIL" ? (
                                    <Button variant="text" color="primary" style={{ width: "100%", maxWidth: "110px" }} onClick={() => rollbackDapp(prop.data.dapp_id)}>
                                        Rollback
                                    </Button>
                                ) : null}
                            </Col>
                            <Col xs={8} style={{ justifyContent: "right", display: "flex" }}>
                                {prop.data.status === "CREATE_FAIL" ? (
                                    <Button variant="outlined" color="secondary" style={{ width: "100%", maxWidth: "110px", marginRight: "10px" }} onClick={() => reCreateDapp(prop.data.dapp_id)}>
                                        Recreate
                                    </Button>
                                ) : prop.data.status === "UPDATE_FAIL" ? (
                                    <Button variant="outlined" color="secondary" style={{ width: "100%", maxWidth: "110px", marginRight: "10px" }} onClick={() => reUpdateDapp(prop.data.dapp_id)}>
                                        Re-Update
                                    </Button>
                                ) : (
                                    <Button variant="outlined" color="secondary" style={{ width: "100%", maxWidth: "110px", marginRight: "10px" }} onClick={() => reDeleteDapp(prop.data.dapp_id)}>
                                        Re-Delete
                                    </Button>
                                )}
                                <Button variant="contained" color="secondary" style={{ width: "100%", maxWidth: "110px" }} onClick={() => deleteDapp(prop.data.dapp_id)}>
                                    Terminate
                                </Button>
                            </Col>
                        </Row>
                    ) : (
                        <Row>
                            <Col xs={4}>
                                <Button disabled={prop.data.status.includes("PENDING")} onClick={() => handleDownloadSDK()} variant="text" color="primary" style={{ width: "100%", maxWidth: "110px" }}>
                                    <Download width={24} height={24} />
                                    <span style={{ marginLeft: "5px" }}>SDK</span>
                                </Button>
                            </Col>
                            <Col xs={8} style={{ justifyContent: "right", display: "flex" }}>
                                <Button
                                    disabled={prop.data.status.includes("PENDING")}
                                    variant="outlined"
                                    color="primary"
                                    style={{ width: "100%", maxWidth: "110px", marginRight: "10px" }}
                                    onClick={() => {
                                        dispatch({ type: CURRENT_DAPP, payload: prop.data });
                                        navigate(`${prop.data.dapp_id}`);
                                    }}
                                >
                                    {"Detail"}
                                </Button>

                                <Button
                                    disabled={prop.data.status.includes("PENDING")}
                                    variant="contained"
                                    color="primary"
                                    style={{ width: "100%", maxWidth: "110px" }}
                                    onClick={() => window.open(`${DOCS_DAPP_URL}/${prop.data.dapp_id}/index.html`, "_blank")}
                                >
                                    {"Docs"}
                                </Button>
                            </Col>
                        </Row>
                    )} */}
                </CardBody>
            </Card>
        </Col>
    );
};

export default CardDApp;
