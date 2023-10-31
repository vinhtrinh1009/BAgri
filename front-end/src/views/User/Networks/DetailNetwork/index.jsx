import React, { useState, Fragment, useEffect } from "react";
import { Edit3, Info, Plus, Server, Trash2 } from "react-feather";
import { useDispatch, useSelector } from "react-redux";

import { Container, Card, CardBody, Media } from "reactstrap";
import { Row, Col } from "react-bootstrap";
import { networkActions } from "src/redux/User/Networks/reducer";
import CardDAppNetwork from "./components/CardDAppNetwork";
import { useNavigate, useParams } from "react-router";
import { Button } from "@material-ui/core";
import errorImg from "src/assets/images/search-not-found.png";
import { CORE_SERVICE_URL } from "src/constant/config";
import { getToken } from "src/utils/token";
import axios from "axios";
import { networkStatus } from "../../../../constant/networkStatus";
import { statusNetworkClassName } from "../../../../constant/statusNetworkClassName";
import { imagePath } from "../../../../constant/imagePath";
import ManageResource from "./ManageResource/ManageResource";
import { Divider } from "@mui/material";
import ModalAddOrganization from "./ModalAddOrganization/ModalAddOrganization";

const DetailNetwork = (props) => {
    let { networkId } = useParams();
    const navigate = useNavigate();
    const [network, setNetwork] = useState();
    const dispatch = useDispatch();
    const userData = useSelector((stores) => stores.User.user);
    const [organizationModal, setOrganizationModal] = useState(false);
    async function getNetworkById(params) {
        const response = await axios({
            method: "GET",
            url: `${CORE_SERVICE_URL}/networks/${params}`,
            headers: {
                "Content-Type": "application/json",
                Authorization: getToken(),
            },
            timeout: 30000,
        });
        setNetwork(response.data.data[0]);
        return response;
    }

    useEffect(() => {
        getNetworkById(networkId);
        // dispatch(networkActions.getNetworkById(networkId))
    }, []);

    const handleDeleteNetwork = () => {
        navigate("/networks");
        dispatch(networkActions.deleteNetwork(network.network_id));
    };
    const handleEditNetwork = () => {
        setOrganizationModal(true);
    };
    const alertDelete = () => {
        const r = window.confirm("Are you sure you want to delete it?");
        if (r == true) {
            handleDeleteNetwork();
        }
    };

    return network ? (
        <Fragment>
            <Container style={{ maxWidth: "1605px", margin: "0 auto" }}>
                <div style={{ padding: "30px 0px" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
                        <h5 style={{ display: "flex", alignItems: "center" }}>
                            <div className="avatars mr-3">
                                <div className="avatar">
                                    <Media body className="img-60 " src={network.blockchain_type == 'fabric' ? imagePath.fabric
                                                                        : network.blockchain_type == 'sawtooth' ? imagePath.sawtooth
                                                                        : network.blockchain_type == 'ethereum' && network.node_infrastructure.name == 'bsc' ? imagePath.bsc
                                                                        : network.blockchain_type == 'ethereum' && network.node_infrastructure.name == 'bsct' ? imagePath.bsc
                                                                        : network.blockchain_type == 'ethereum' && network.node_infrastructure.name == 'ftm' ? imagePath.ftm
                                                                        : network.blockchain_type == 'ethereum' && network.node_infrastructure.name == 'ftmt' ? imagePath.ftm
                                                                        : imagePath.ethereum} alt="#" />
                                    {/* <Media body className="img-60 " src={imagePath[network.blockchain_type] || imagePath.fabric} alt="#" /> */}
                                </div>
                            </div>
                            <div style={{ textTransform: "capitalize" }}>
                                {network.name}
                                <div className="state">
                                    <div className={`dot-notify ${statusNetworkClassName[network.status] || statusNetworkClassName.ELSE}`}></div>
                                    <div>{networkStatus[network.status] || networkStatus.ELSE}</div>
                                </div>
                            </div>
                        </h5>
                        <div className="media-body text-right">
                            {network.blockchain_type === "fabric" ? (
                                <>
                                    <Button onClick={() => handleEditNetwork()} variant="contained" color="primary" className="mr-2">
                                        <Edit3 width={17} height={17} className="mr-2" />
                                        {"Edit"}
                                    </Button>
                                    <ModalAddOrganization
                                        idNetwork={networkId}
                                        open={organizationModal}
                                        handleCloseModal={() => setOrganizationModal(false)}
                                        organizations={network.blockchain_peer_config.organizations}
                                    />
                                </>
                            ) : null}

                            <Button onClick={() => alertDelete()} variant="outlined" color="primary" style={{ textTransform: "none" }}>
                                <Trash2 width={17} height={17} className="mr-2" />
                                Delete
                            </Button>
                        </div>
                    </div>
                    <Card>
                        <CardBody style={{ padding: "30px" }}>
                            <Row style={{ marginBottom: "60px" }}>
                                <Col xxl={3} xs={12}>
                                    <h6 style={{ color: "#8CB8D8", fontSize: "16px" }}>BASIC INFORMATION</h6>
                                </Col>
                                <Col xxl={3} xs={4}>
                                    <div style={{ opacity: "0.65" }}>Name</div>
                                    <strong>{network.name}</strong>
                                </Col>
                                <Col xxl={3} xs={4}>
                                    <div style={{ opacity: "0.65" }}>Type</div>
                                    <strong>
                                        {network.blockchain_type === 'fabric' ? 'Hyperledger Fabric'
                                        : network.blockchain_type === 'sawtooth' ? 'Hyperledger Sawtooth'
                                        : network.blockchain_type === 'ethereum' ? 'Ethereum'
                                        : network.blockchain_type}
                                    </strong>
                                </Col>
                                <Col xxl={3} xs={4}>
                                    <div style={{ opacity: "0.65" }}>Consensus</div>
                                    <strong>
                                        {network.consensus === 'raft' ? 'RAFT'
                                        :network.consensus === 'poet' ? 'PoET'
                                        :network.consensus === 'pbft' ? 'PBFT'
                                        :network.consensus === 'pow' ? 'PoW'
                                        :network.consensus}
                                    </strong>
                                </Col>
                            </Row>
                            <Row style={{ marginBottom: "60px" }}>
                                <Col xxl={3} xs={12}>
                                    <h6
                                        style={{
                                            color: "#8CB8D8",
                                            fontSize: "16px",
                                            width: "100%",
                                            textOverflow: "ellipsis",
                                            whiteSpace: "nowrap",
                                            overflow: "hidden",
                                            textAlign: "left",
                                        }}
                                    >
                                        MANAGEMENT INFORMATION
                                    </h6>
                                    <br />
                                </Col>
                                <Col xxl={3} xs={4}>
                                    <div style={{ opacity: "0.65" }}>Owner</div>
                                    <strong>{userData.full_name}</strong>
                                </Col>
                                <Col xxl={3} xs={8}>
                                    <div style={{ opacity: "0.65" }}>Network ID</div>
                                    <strong
                                        style={{
                                            width: "100%",
                                            textOverflow: "ellipsis",
                                            whiteSpace: "nowrap",
                                            overflow: "hidden",
                                            textAlign: "left",
                                        }}
                                    >
                                        {network.network_id}
                                    </strong>
                                </Col>
                            </Row>
                            {network.blockchain_type === "ethereum" ? (
                                <></>
                            ) : (
                                <>
                                    <Row style={{ marginBottom: "60px" }}>
                                        <Col xxl={3} xs={12}>
                                            <h6 style={{ color: "#8CB8D8", fontSize: "16px" }}>TOTAL CLUSTER CAPACITY</h6>
                                            <br />
                                        </Col>
                                        <Col xxl={3} xs={4}>
                                            <div style={{ opacity: "0.65" }}>CPU</div>
                                            <strong>{network.node_infrastructure?.node_plan?.cpu || "#"} CPU</strong>
                                        </Col>
                                        <Col xxl={3} xs={4}>
                                            <div style={{ opacity: "0.65" }}>Memory</div>
                                            <strong>{network?.node_infrastructure?.node_plan?.ram || "#"} GB</strong>
                                        </Col>
                                        {/* <Col xxl={3} xs={4}>
                                            <div style={{ opacity: "0.65" }}>Disk</div>
                                            <strong>{network?.node_infrastructure?.node_plan?.disk || "#"} GB</strong>
                                        </Col> */}
                                    </Row>
                                    {network && network.blockchain_type === "sawtooth" ? (
                                        <Row style={{ marginBottom: "30px" }}>
                                            <Col xxl={3} xs={12}>
                                                <h6 style={{ color: "#8CB8D8", fontSize: "16px" }}>BLOCKCHAIN PEER CONFIG</h6>
                                                <br />
                                            </Col>
                                            <Col xxl={3} xs={12}>
                                                <div style={{ opacity: "0.65" }}>Number Of Peers</div>
                                                <strong>{network.blockchain_peer_config.number_peer}</strong>
                                            </Col>
                                        </Row>
                                    ) : (
                                        <Row style={{ marginBottom: "30px" }}>
                                            <Col xxl={3} xs={12}>
                                                <h6 style={{ color: "#8CB8D8", fontSize: "16px" }}>BLOCKCHAIN PEER CONFIG</h6>
                                                <br />
                                            </Col>
                                            <Col xxl={9} xs={12}>
                                                {network.blockchain_peer_config.organizations &&
                                                    network.blockchain_peer_config.organizations.map((value, key) => {
                                                        return (
                                                            <Row className="mb-2" key={"organi" + key}>
                                                                <Col xs={4}>
                                                                    <div style={{ opacity: "0.65" }}>Organization {key + 1}</div>
                                                                    <strong>{value.name}</strong>
                                                                </Col>
                                                                <Col xs={8}>
                                                                    <div style={{ opacity: "0.65" }}>Number Of Peers</div>
                                                                    <strong>{value.number_peer}</strong>
                                                                </Col>
                                                            </Row>
                                                        );
                                                    })}
                                            </Col>
                                        </Row>
                                    )}
                                </>
                            )}
                            <Divider />
                            <Row className="m-t-30">
                                <Col className="col-md-12">
                                    <div className="d-flex" style={{ justifyContent: "space-between", alignItems: "center" }}>
                                        <h6 style={{ color: "#8CB8D8" }}>DAPP IN NETWORK</h6>
                                        <div className="d-flex" style={{ alignItems: "center" }}>
                                            <div className="state mr-4">
                                                <div className="dot-notify dot-notification-green" style={{ width: "12px", height: "12px" }} />
                                                <div style={{ fontSize: "14px" }}>Running</div>
                                            </div>
                                            <div className="state mr-4">
                                                <div className="dot-notify dot-notification-yellow" style={{ width: "12px", height: "12px" }} />
                                                <div style={{ fontSize: "14px" }}>Pending</div>
                                            </div>
                                            <div className="state">
                                                <div className="dot-notify dot-notification-red" style={{ width: "12px", height: "12px" }} />
                                                <div style={{ fontSize: "14px" }}>Error</div>
                                            </div>
                                        </div>
                                    </div>
                                    <br />
                                    <br />
                                    <div className="flex_box_row">
                                        {network && network.dapps.length === 0 ? (
                                            <Col xs={12} className="text-center">
                                                <img className="img-fluid m-auto" src={errorImg} alt="" />
                                                <h5 style={{ display: "flex", alignItems: "center", justifyContent: "center" }}>This network has no DApp to display !!!</h5>
                                            </Col>
                                        ) : (
                                            <>
                                                {network.dapps.map((value, key) => {
                                                    return <CardDAppNetwork data={value} key={"carddappnetwprk" + key} end={false} order={key} />;
                                                })}
                                            </>
                                        )}
                                    </div>
                                </Col>
                            </Row>
                        </CardBody>
                    </Card>
                    {network.blockchain_type === "ethereum" ? null : (
                        <ManageResource idNetwork={networkId} typeNetwork={network.blockchain_type} organizations={network.blockchain_peer_config?.organizations || []} />
                    )}
                </div>
            </Container>
        </Fragment>
    ) : (
        ""
    );
};

export default DetailNetwork;
