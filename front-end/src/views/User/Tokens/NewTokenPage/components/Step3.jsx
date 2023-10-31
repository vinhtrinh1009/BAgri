import React, { Fragment, useEffect } from "react";
import { Button } from "@mui/material";
import { updateToken } from "src/services/User/tokens";
import { Link } from "react-router-dom";
import { Col, Row } from "reactstrap";
const Step3 = (props) => {
    const token_type = ["ERC-20", "ERC-721"].includes(props.data.contract.token_standard) ? "fungible" : "non_fungible";
    const id = props.data.contract.id;
    console.log(id);
    console.log(token_type);

    useEffect(() => {
        if (!props.data.contract.user_defined_network) {
            updateToken({
                token_type: token_type,
                id: id,
                address: props.data.contract.address,
                network: props.data.network.name,
            }).catch((err) => {
                alert("Something wrong happens. Please try again.");
            });
        }
    }, []);

    const handleFinish = () => {
        window.location.href = `/tokens/${id}/${token_type}`;
    };

    return (
        <div className="mt-5 step_3">
            <div className="d-flex justify-content-center w-100 flex-column align-items-center">
                <div className="mb-3">
                    <h5>Your token is deployed</h5>

                    <Row className="setup_info">
                        <Col md={6}>
                            <span>Name:</span>
                        </Col>
                        <Col md={6}>
                            <span>{props.data.contract.token_name}</span>
                        </Col>
                    </Row>
                    <Row className="setup_info">
                        <Col md={6}>
                            <span>Symbol:</span>
                        </Col>
                        <Col md={6}>
                            <span>{props.data.contract.token_symbol}</span>
                        </Col>
                    </Row>
                    <Row className="setup_info">
                        <Col md={6}>
                            <span>Standard:</span>
                        </Col>
                        <Col md={6}>
                            <span>{props.data.contract.token_standard}</span>
                        </Col>
                    </Row>
                    <Row className="setup_info">
                        <Col md={6}>
                            <span>Address:</span>
                        </Col>
                        <Col md={6}>
                            <span>{props.data.contract.address}</span>
                        </Col>
                    </Row>
                </div>
                <div>
                    <div className="media-body text-center">
                        <Button variant="contained" className="px-2 mb-2 mr-2 text-nowrap" onClick={handleFinish} disableElevation={true}>
                            Finish
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Step3;
