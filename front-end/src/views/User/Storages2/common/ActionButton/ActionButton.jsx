import React, { useRef, useState } from "react";
import { Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, TextField } from "@mui/material";
import { FilePlus, FolderPlus, Plus } from "react-feather";
import { OPEN_SUCCESS_ALERT } from "../../../../../redux/User/Alerts/actionTypes";
import { OPEN_ERROR_ALERT } from "../../../../../redux/User/Alerts/actionTypes";
import { storageService } from "../../../../../services/User/storages";
import { storageActionTypes } from "../../../../../redux/User/Storages/storageActionType";
import { useDispatch, useSelector } from "react-redux";

export default function ActionButton() {
    const storageData = useSelector((stores) => stores.Storage);
    const dispatch = useDispatch();
    const actionButton = useRef(null);
    const clickAwayActionArea = useRef(null);
    const upLoadFileRef = useRef(null);
    const upLoadFolderRef = useRef(null);
    const [newFolderName, setNewFolderName] = useState("");
    const [open, setOpen] = useState(false);

    const handleClickOpenModal = () => {
        setOpen(true);
    };
    const handleCloseModal = () => {
        setOpen(false);
    };
    const handleCreateFolder = async () => {
        const response = await storageService.createNewBlankFolder({ name: newFolderName, parent_id: storageData.data.folder_id, shared: [] });
        if (response.status === "success") {
            dispatch({ type: storageActionTypes.activeReloadData });
            setTimeout(() => {
                dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Create success!" } });
                setNewFolderName("");
            }, 500);
        } else {
            dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Create fail!" } });
        }
        handleCloseModal();
    };

    function optItemClick(e) {
        e.stopPropagation();
        clickAwayActionArea.current.style.display = "none";
        actionButton.current.style.display = "none";
    }
    function uploadFileButtonClick() {
        upLoadFileRef.current.click();
    }
    function uploadFolderButtonClick() {
        upLoadFolderRef.current.click();
    }
    async function uploadFileHandle(e) {
        let bodyFormData = new FormData();
        bodyFormData.append("shared", []);
        bodyFormData.append("upload_file", e.target.files[0]);
        const response = await storageService.uploadFile(storageData.data.folder_id, bodyFormData);
        if (response.status === "success") {
            dispatch({ type: storageActionTypes.activeReloadData });
            setTimeout(() => {
                dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Upload success!" } });
            }, 800);
        } else {
            dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Upload fail!" } });
        }
    }
    async function uploadFolderHandle(e) {
        let bodyFormData = new FormData();
        bodyFormData.append("shared", []);
        for (let i = 0; i < e.target.files.length; i++) {
            bodyFormData.append(`upload_folder[${i}]`, e.target.files[i]);
        }
        const response = await storageService.uploadFolder(storageData.data.folder_id, bodyFormData);
        if (response.status === "success") {
            dispatch({ type: storageActionTypes.activeReloadData });
            setTimeout(() => {
                dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Upload success!" } });
            }, 800);
        } else {
            dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Upload fail!" } });
        }
    }
    return (
        <>
            <Button
                variant="contained"
                style={{ width: "116px", height: "38px" }}
                onClick={() => {
                    if (actionButton.current.style.display === "none") {
                        actionButton.current.style.display = "block";
                        clickAwayActionArea.current.style.display = "block";
                    } else {
                        actionButton.current.style.display = "none";
                        clickAwayActionArea.current.style.display = "none";
                    }
                }}
            >
                <Plus style={{ marginRight: "12px" }} /> Action
            </Button>
            <div ref={clickAwayActionArea} className="clickaway_area" onClick={optItemClick}></div>
            <div ref={actionButton} className="menu_more_option" style={{ display: "none", top: "70px" }}>
                <div
                    className="opt_item"
                    onClick={(e) => {
                        uploadFileButtonClick();
                        optItemClick(e);
                    }}
                >
                    <FilePlus width={17} height={17} style={{ marginLeft: "15px", marginRight: "15px" }} /> Upload new file
                    <input id="inputUploadFile" ref={upLoadFileRef} className="hidden_bg_upload" type="file" name="uploadFile" onChange={uploadFileHandle} />
                </div>
                <div
                    className="opt_item"
                    onClick={(e) => {
                        uploadFolderButtonClick();
                        optItemClick(e);
                    }}
                >
                    <FolderPlus width={17} height={17} style={{ marginLeft: "15px", marginRight: "15px" }} /> Upload new folder
                    <input id="inputUploadFolder" ref={upLoadFolderRef} type="file" webkitdirectory="true" mozdirectory="true" className="hidden_bg_upload" onChange={uploadFolderHandle} />
                </div>
                <div
                    className="opt_item"
                    id="createNewFolderBtn"
                    onClick={(e) => {
                        handleClickOpenModal();
                        optItemClick(e);
                    }}
                >
                    <FolderPlus width={17} height={17} style={{ marginLeft: "15px", marginRight: "15px" }} /> Create new folder
                </div>
            </div>
            <Dialog maxWidth={"xs"} open={open} fullWidth onClose={handleCloseModal}>
                <DialogTitle>Create New Folder</DialogTitle>
                <DialogContent style={{ paddingTop: "20px" }}>
                    <TextField
                        value={newFolderName}
                        autoFocus
                        label="Folder name"
                        type="text"
                        fullWidth
                        variant="outlined"
                        onChange={(e) => {
                            setNewFolderName(e.target.value);
                        }}
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseModal}>Cancel</Button>
                    <Button onClick={handleCreateFolder} disabled={newFolderName === ""}>
                        Create
                    </Button>
                </DialogActions>
            </Dialog>
        </>
    );
}
