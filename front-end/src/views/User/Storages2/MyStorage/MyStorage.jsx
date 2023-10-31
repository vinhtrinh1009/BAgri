import React, { useEffect, useRef, useState } from "react";
import { Apps } from "@material-ui/icons";
import { Col, Container, Row } from "react-bootstrap";
import { List, Search } from "react-feather";
import StoragesData from "../common/StoragesData/StoragesData";
import { useDispatch, useSelector } from "react-redux";
import { storageActionTypes } from "../../../../redux/User/Storages/storageActionType";
import { storageService } from "../../../../services/User/storages.js";
import { OPEN_ERROR_ALERT } from "../../../../redux/User/Alerts/actionTypes";
import { exchangeSizeValue } from "../../../../utils/commonFunction";
import { OPEN_SUCCESS_ALERT } from "../../../../redux/User/Alerts/actionTypes";
import ActionButton from "../common/ActionButton/ActionButton";

var Knob = require("knob");

function getPercentageUsed(num) {
    const percentage = num / (1024 * 1024 * 1024); // x/tong 100Gb
    if (percentage < 10) {
        return +(Math.round(percentage + "e+4") + "e-4");
    } else if (percentage < 100) {
        return +(Math.round(percentage + "e+3") + "e-3");
    } else {
        return +(Math.round(percentage + "e+2") + "e-2");
    }
}

export default function MyStorage() {
    const storageData = useSelector((stores) => stores.Storage);
    const dispatch = useDispatch();

    useEffect(() => {
        (async () => {
            const res = await storageService.getUserStorages();
            if (res.status === "success") {
                dispatch({ type: storageActionTypes.setStorageData, payload: { ...res.data.user_folder, path: [{ name: "My storage", folder_id: "" }] } });
            } else {
                dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Have error when load data!" } });
            }
        })();
    }, [storageData.reload_data_storage]);
    useEffect(() => {
        var displayInputDisable = Knob({
            className: "review",
            thickness: 0.2,
            width: 52,
            fgColor: "#1998F4",
            bgColor: "#E6E6E6",
            lineCap: "round",
            readOnly: true,
            displayPrevious: false,
            value: getPercentageUsed(storageData.data.total_size),
        });
        document.getElementById("displayInputDisable").innerHTML = "";
        document.getElementById("displayInputDisable").appendChild(displayInputDisable);
    }, [storageData.data.total_size]);

    return (
        <Container className="my_storage" style={{ maxWidth: "1605px", margin: "0 auto" }}>
            <div className="my_storage_header">
                <div className="my_storage_header_title">My Storage</div>
                <div className="my_storage_header_consumption">
                    <div style={{ marginRight: "19px" }}>
                        <div>
                            <span className="my_storage_header_consumption_text" style={{ opacity: "0.6", marginRight: "6px" }}>
                                Total Memory
                            </span>
                            <span className="my_storage_header_consumption_text" style={{ fontWeight: "bold" }}>
                                {exchangeSizeValue(storageData.data.total_size)}/100 Gb
                            </span>
                        </div>
                        <div className="my_storage_header_consumption_text" style={{ textAlign: "right", color: "#1998F4", marginTop: "13px" }}>
                            Buy More
                        </div>
                    </div>
                    <div id="displayInputDisable"></div>
                </div>
            </div>
            <Row className="action_part">
                <Col lg={6}>
                    <div className="action_part_search_bar">
                        <span className="action_part_search_bar_icon">
                            <Search />
                        </span>
                        <input type="text" placeholder="Find in storage ..." />
                    </div>
                </Col>
                <Col lg={6}>
                    <div style={{ height: "100%", display: "flex", alignItems: "end", justifyContent: "right", position: "relative" }}>
                        <span style={{ opacity: 0.65, marginRight: "20px", cursor: "pointer" }} onClick={() => dispatch({ type: storageActionTypes.toggleViewMode })}>
                            {storageData.isGridViewMode ? <List /> : <Apps />}
                        </span>
                        <ActionButton />
                    </div>
                </Col>
            </Row>
            <StoragesData onRightClick={true} />
        </Container>
    );
}
