import React, { useEffect, useState } from "react";
import { Button, Dialog, DialogActions, DialogContent, DialogTitle, Divider } from "@mui/material";
import { useDispatch, useSelector } from "react-redux";
import { storageService } from "../../../../../services/User/storages";
import { storageActionTypes } from "../../../../../redux/User/Storages/storageActionType";
import { OPEN_ERROR_ALERT } from "../../../../../redux/User/Alerts/actionTypes";
import { Col, Row } from "reactstrap";

const typeData = {
    STANDARD_FOLDER: "Standard folder",
};
export default function DialogDetailFolder(props) {
    const { open = false, handleCloseModal = () => {}, typeContent = "" } = props;
    const item_selected = useSelector((stores) => stores.Storage.item_selected);
    const [detail, setDetail] = useState({});
    const dispatch = useDispatch();
    useEffect(() => {
        (async () => {
            if (open) {
                if (item_selected.type == "folder") {
                    if (item_selected.isOwner) {
                        const res = await storageService.getDataFolder(item_selected.id);
                        if (res.status === "success") {
                            console.log(res.data.folder);
                            setDetail(res.data.folder);
                        } else {
                            dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Have error when load data!" } });
                        }
                    } else {
                        const res = await storageService.getDataPlatformFolder(item_selected.id);
                        if (res.status === "success") {
                            console.log(res.data.folder);
                            setDetail({ ...res.data.folder, child_files: res.data.folder.child_files, child_folders: res.data.folder.child_folders });
                        } else {
                            dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Have error when load data!" } });
                        }
                    }
                } else {
                    // const res = await storageService.getD(item_selected.id);
                    // if (res.status === "success") {
                    //     console.log(res.data.folder );
                    // } else {
                    //     dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Have error when load data!" } });
                    // }
                }
            }
        })();
    }, [open]);
    return (
        <Dialog maxWidth={"xs"} open={open} fullWidth onClose={handleCloseModal} onClick={(e) => e.stopPropagation()} onContextMenu={(e) => e.stopPropagation()} style={{ zIndex: 10000 }}>
            <DialogTitle>Detail information</DialogTitle>
            <DialogContent>
                <Row style={{ margin: "10px 0px" }}>
                    <Col xs={4}>Owner:</Col>
                    <Col xs={8} style={{ fontWeight: "bold" }}>
                        {detail.owner?.full_name} - {detail.owner?.username}
                    </Col>
                </Row>
                <Divider></Divider>
                <Row style={{ margin: "10px 0px" }}>
                    <Col xs={4}>Name:</Col>
                    <Col xs={8} style={{ fontWeight: "bold" }}>
                        {detail.name}
                    </Col>
                </Row>
                <Row style={{ margin: "10px 0px" }}>
                    <Col xs={4}>Type:</Col>
                    <Col xs={8} style={{ fontWeight: "bold" }}>
                        {typeData[detail.type]}
                    </Col>
                </Row>
            </DialogContent>
            <DialogActions>
                <Button variant="outlined" color="secondary" onClick={handleCloseModal}>
                    Close
                </Button>
            </DialogActions>
        </Dialog>
    );
}
