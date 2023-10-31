import React from "react";
import { Container, Row, Col, Card, CardBody } from "reactstrap";
// import { Link } from 'react-router-dom'
// import { PlusSquare } from 'react-feather'
import CardToken from "./components/CardToken";
import AddBoxOutlinedIcon from "@mui/icons-material/AddBoxOutlined";
import Button from "@mui/material/Button";
import { AddCircleOutline } from "@material-ui/icons";
import { useNavigate } from "react-router";

const MyTokensPage = () => {
    const navigate = useNavigate();

    return (
        <>
            <Container style={{ maxWidth: "1605px", margin: "0px auto", paddingTop: "30px" }}>
                <Row>
                    <Col sm={4} style={{ display: "flex", alignItems: "center", justifyContent: "left" }}>
                        <strong style={{ font: "normal normal bold 24px/28px Roboto" }}>My Tokens</strong>
                    </Col>
                    <Col sm={8} style={{ display: "flex", alignItems: "center", justifyContent: "right" }}>
                        <Button
                            variant="contained"
                            onClick={() => {
                                navigate("/tokens/new");
                            }}
                        >
                            <AddCircleOutline className="mr-2" /> New Token
                        </Button>
                    </Col>
                </Row>

                <Card style={{ marginTop: "25px" }}>
                    <CardBody style={{ padding: "19px 30px" }}>
                        <CardToken />
                    </CardBody>
                </Card>
            </Container>
        </>
    );
};

export default MyTokensPage;
