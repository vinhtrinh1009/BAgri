import React, { useRef, useState } from "react";
import { Button, Dialog, DialogActions, DialogContent, DialogTitle, Divider, TextField } from "@mui/material";
import { createNetworkResource } from "../../../../../services/User/networks";
import { useDispatch } from "react-redux";
import { OPEN_SUCCESS_ALERT } from "../../../../../redux/User/Alerts/actionTypes";
import { OPEN_ERROR_ALERT } from "../../../../../redux/User/Alerts/actionTypes";
import InputNumber from "../../NewNetwork/components/InputNumber";
import { isOnlyLowerLetterAndNumber, isPositiveNumber } from "../../../../../utils/stringhandle";
import { updateNetwork } from "../../../../../services/User/networks";
import { useNavigate } from "react-router";

export default function ModalAddOrganization(props) {
    const { idNetwork = "", open = false, handleCloseModal = () => {}, organizations = [], reloadListResource = () => {} } = props;
    const [dataPost, setDataPost] = useState({ update_type: "new_organization", config: { name: "", number_peer: 1 } });
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const [errorName, setErrorName] = useState("");

    function changeNodeName(text) {
        setDataPost((prev) => {
            return {
                ...prev,
                config: {
                    ...prev.config,
                    name: text,
                },
            };
        });
        checkOrgName(text);
    }
    function changeNumberOfPeer(text) {
        setDataPost((prev) => {
            return {
                ...prev,
                config: {
                    ...prev.config,
                    number_peer: text,
                },
            };
        });
    }
    function checkSameOrgName(name) {
        const orgLength = organizations.length;
        for (let i = 0; i < orgLength; i++) {
            if (organizations[i].name === name && name !== "") {
                return true;
            }
        }
        return false;
    }
    function checkOrgName(name) {
        if (isOnlyLowerLetterAndNumber(name)) {
            if (isNaN(name[0])) {
                if (!checkSameOrgName(name)) {
                    setErrorName("");
                    return true;
                } else {
                    setErrorName("This name already used!");
                }
            } else {
                setErrorName("Only lower letter and number. Letter beginning!");
            }
        } else {
            setErrorName("Only lower letter and number. Letter beginning!");
        }
        return false;
    }
    function checkCreateCondition() {
        return dataPost.config.name && isPositiveNumber(dataPost.config.number_peer) && errorName == "";
    }
    async function createNewOrganization() {
        const filter_data_post = {
            ...dataPost,
            config: { ...dataPost.config, number_peer: Number(dataPost.config.number_peer) },
        };
        const res = await updateNetwork(idNetwork, filter_data_post);
        if (res.status === "success") {
            navigate("/networks");
        } else {
            dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Have error! " + res.error } });
        }
    }
    return (
        <Dialog maxWidth={"xs"} open={open} fullWidth onClose={handleCloseModal} onClick={(e) => e.stopPropagation()} onContextMenu={(e) => e.stopPropagation()} style={{ zIndex: 10000 }}>
            <DialogTitle>Add new organization</DialogTitle>
            <DialogContent style={{ paddingTop: "10px" }}>
                <div style={{ marginBottom: "31px", position: "relative" }}>
                    <TextField
                        error={errorName != ""}
                        value={dataPost.config.name}
                        label="Organization name"
                        size="small"
                        type="text"
                        fullWidth
                        variant="outlined"
                        onChange={(e) => {
                            changeNodeName(e.target.value);
                        }}
                    />
                    <div style={{ fontSize: "small", color: "red", position: "absolute" }}>{errorName}</div>
                </div>

                <InputNumber
                    value={dataPost.config.number_peer}
                    label="Number of peers"
                    type="text"
                    fullWidth
                    onlyPositive={true}
                    variant="outlined"
                    OnChange={(e) => {
                        changeNumberOfPeer(e.target.value);
                    }}
                />
            </DialogContent>
            <DialogActions>
                <Button className="mr-1" variant="outlined" color="secondary" onClick={handleCloseModal}>
                    Cancel
                </Button>
                <Button className="mr-3" variant="contained" onClick={createNewOrganization} disabled={!checkCreateCondition()}>
                    Create
                </Button>
            </DialogActions>
        </Dialog>
    );
}
