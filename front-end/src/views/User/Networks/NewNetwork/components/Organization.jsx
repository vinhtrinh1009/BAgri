import { Remove } from "@material-ui/icons";
import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Col, Row } from "reactstrap";
import { DELETE_ORGANIZATIONS, UPDATE_ORGANIZATIONS } from "../../../../../redux/User/Networks/actionTypes";
import { TextField } from "@mui/material";
import InputNumber from "./InputNumber";
import { isOnlyLowerLetterAndNumber } from "../../../../../utils/stringhandle";

export default function Organization(props) {
    const dispatch = useDispatch();
    const { index } = props;
    const organizations = useSelector((state) => state.Network.organizations);
    let helperText = "";
    const handleChangeOrganizationName = (event) => {
        let temp = [...organizations];
        temp[index].name = event.target.value;
        dispatch({ type: UPDATE_ORGANIZATIONS, payload: temp });
    };

    const handleChangeNumberOfPeers = (event) => {
        let temp = [...organizations];
        temp[index].number_peer = parseInt(event.target.value);
        dispatch({ type: UPDATE_ORGANIZATIONS, payload: temp });
    };
    const handleDeleteOrganization = () => {
        let temp = organizations.filter((value, i) => i != index);
        dispatch({ type: DELETE_ORGANIZATIONS, payload: temp });
    };
    function checkSameOrgName() {
        const orgLength = organizations.length;
        for (let i = 0; i < orgLength; i++) {
            if (i != index && organizations[i].name === organizations[index].name && organizations[i].name !== "") {
                return true;
            }
        }
        return false;
    }
    function checkOrgName() {
        if (isOnlyLowerLetterAndNumber(organizations[index]?.name)) {
            if (isNaN(organizations[index]?.name[0])) {
                if (!checkSameOrgName()) {
                    helperText = "";
                    return true;
                } else {
                    helperText = "This name already used!";
                }
            } else {
                helperText = "Only lower letter and number. Letter beginning!";
            }
        } else {
            helperText = "Only lower letter and number. Letter beginning!";
        }
        return false;
    }
    return (
        <Row className="oganization">
            <Col md={8}>
                <TextField
                    error={!checkOrgName()}
                    inputMode="text"
                    label={`Organization ${index + 1} Name`}
                    variant="filled"
                    fullWidth
                    onChange={handleChangeOrganizationName}
                    defaultValue={organizations[index]?.name}
                    required
                    size="small"
                />
                <div style={{ marginBottom: "31px", fontSize: "small", color: "red", position: "absolute" }}>{helperText}</div>
            </Col>
            <Col md={4}>
                <InputNumber
                    label={`Number Peers`}
                    variant="filled"
                    OnChange={handleChangeNumberOfPeers}
                    defaultValue={organizations[index]?.number_peer}
                    onlyPositive={true}
                    required={true}
                    style={{ marginBottom: "36px" }}
                />
            </Col>
            <span className="remove_btn" style={{ display: organizations.length == 1 ? "none" : "" }} onClick={handleDeleteOrganization}>
                <Remove />
            </span>
        </Row>
    );
}
