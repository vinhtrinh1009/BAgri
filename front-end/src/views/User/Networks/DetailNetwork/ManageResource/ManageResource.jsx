import React, { useEffect, useState } from "react";
import { Button, Divider } from "@mui/material";
import { Card, CardBody, Col, Row } from "reactstrap";
import { Download, Plus } from "react-feather";
import ModalAddNode from "../ModalAddNode/ModalAddNode";
import { getNetworkResources } from "../../../../../services/User/networks";
import { statusNetworkClassName } from "../../../../../constant/statusNetworkClassName";
import { networkStatus } from "../../../../../constant/networkStatus";
import { storageService } from "../../../../../services/User/storages";
import FileSaver from "file-saver";
import { OPEN_SUCCESS_ALERT } from "../../../../../redux/User/Alerts/actionTypes";
import { OPEN_ERROR_ALERT } from "../../../../../redux/User/Alerts/actionTypes";
import { useDispatch } from "react-redux";
import errorImg from "src/assets/images/search-not-found.png";

export default function ManageResource(props) {
    const dispatch = useDispatch();
    const { idNetwork, typeNetwork, organizations = [] } = props;
    const [openModal, setOpenModal] = useState(false);
    const [listResource, setListResource] = useState([]);
    function closeModal() {
        setOpenModal(false);
    }
    async function getListResource() {
        const res = await getNetworkResources(idNetwork);
        setListResource(res.data);
    }
    useEffect(() => {
        getListResource();
    }, []);

    async function downloadItem(fileName, idNode) {
        const res = await storageService.downloadFolder(idNode);
        if (res.status === 200) {
            var blob = new Blob([res.data], { type: "application/octet-stream" });
            FileSaver.saveAs(blob, `${fileName}.zip`);
            setTimeout(() => {
                dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Download done!" } });
            }, 600);
        } else {
            dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Have an error occurred! Action fail!" } });
        }
    }
    return (
        <Card style={{ marginBottom: "0px" }}>
            <CardBody style={{ padding: "30px" }} className="manage_resource">
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                    <h6 style={{ color: "#8CB8D8", fontSize: "16px" }}>MANAGE RESOURCE</h6>
                    <Button onClick={() => setOpenModal(true)} variant="contained" color="primary">
                        <Plus width={17} height={17} className="mr-2" />
                        {"Add node"}
                    </Button>
                </div>
                {listResource && listResource.length === 0 ? (
                    <Col xs={12} className="text-center">
                        <img className="img-fluid m-auto" src={errorImg} alt="" />
                        <h5 style={{ display: "flex", alignItems: "center", justifyContent: "center" }}>This network has no resource to display !!!</h5>
                    </Col>
                ) : (
                    < div className="resource_table" style={{ marginTop: "30px" }}>
                        <Row className="header_table">
                            <Col xs={4}>Name</Col>
                            <Col xs={2}>Status</Col>
                            <Col xs={2}>{typeNetwork === "sawtooth" ? "" : "Organization Name"} </Col>
                            <Col xs={2}>Host</Col>
                            <Col xs={2}>Port</Col>
                        </Row>
                        {listResource.map((item, index) => {
                            return (
                                <Row className="row_table" key={"manageResource" + item.resource_id + index}>
                                    <Col xs={4}>{item.resource_name}</Col>
                                    <Col xs={2}>
                                        <div className="state ">
                                            <div className={`dot-notify ${statusNetworkClassName[item.status] || statusNetworkClassName.ELSE}`} style={{ width: "12px", height: "12px" }} />
                                            <div style={{ fontSize: "14px" }}>{networkStatus[item.status] || networkStatus.ELSE}</div>
                                        </div>
                                    </Col>
                                    <Col xs={2}>{item.resource_config.organization_name || ""}</Col>
                                    <Col xs={2}>{item.resource_config.host}</Col>
                                    <Col xs={1}>{item.resource_config.port || "#"}</Col>
                                    <Col xs={1} style={{ textAlign: "right" }}>
                                        <span className="storage_icon_function" title="download config" onClick={() => downloadItem(item.resource_name, item.resource_folder_id)}>
                                            <Download />
                                        </span>
                                    </Col>
                                </Row>
                            );
                        })}
                    </div>
                )}

            <ModalAddNode idNetwork={idNetwork} open={openModal} handleCloseModal={closeModal} typeNetwork={typeNetwork} reloadListResource={getListResource} organizations={organizations} />
        </CardBody>
        </Card >
    );
}
