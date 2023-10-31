import React, { useState } from "react";
import { Button, Dialog, DialogActions, DialogContent, DialogTitle, TextField, List, ListItem, ListItemButton, ListItemIcon, ListItemText, IconButton } from "@mui/material";
import { useSelector } from "react-redux";
import { useEffect } from "react";
import { storageService } from "../../../../../services/User/storages";
import { OPEN_SUCCESS_ALERT } from "../../../../../redux/User/Alerts/actionTypes";
import { OPEN_ERROR_ALERT } from "../../../../../redux/User/Alerts/actionTypes";
import { useDispatch } from "react-redux";
import { storageActionTypes } from "../../../../../redux/User/Storages/storageActionType";
import { Folder, ChevronRight, ChevronLeft } from "@material-ui/icons";

export default function DialogMultiContent(props) {
    const { open = false, handleCloseModal = () => {}, typeContent = "" } = props;
    const storageData = useSelector((stores) => stores.Storage);
    const dispatch = useDispatch();
    const [folderName, setFolderName] = useState("");
    const [desModalData, setDesModalData] = useState({ listFolder: [], parentId: "root", selected: "", currentFolderName: "My Storage", loading: true });
    useEffect(() => {
        if (open) {
            if (typeContent === "rename") {
                setFolderName(storageData.item_selected.name || "");
            } else {
                (async () => {
                    const response = await storageService.getUserStorages();
                    if (response.status === "success") {
                        setDesModalData({ listFolder: response.data.user_folder.child_folders, parentId: "root", selected: "", currentFolderName: "My Storage", loading: false });
                    } else {
                        setDesModalData({ listFolder: [], parentId: "root", selected: "", currentFolderName: "My Storage", loading: false });
                        dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Fail to load data!" } });
                    }
                })();
            }
        }
    }, [open]);
    const handleRenameItem = async () => {
        if (storageData.item_selected.type === "folder") {
            const res = await storageService.renameFolder(storageData.item_selected.id, { name: folderName });
            if (res.status === "success") {
                dispatch({ type: storageActionTypes.activeReloadData });
                setTimeout(() => {
                    dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Rename done!" } });
                }, 600);
            } else {
                dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Rename fail!" } });
            }
            handleCloseModal();
        } else {
            const res = await storageService.renameFile(storageData.item_selected.id, { name: folderName });
            if (res.status === "success") {
                dispatch({ type: storageActionTypes.activeReloadData });
                setTimeout(() => {
                    dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Rename done!" } });
                }, 600);
            } else {
                dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Rename fail!" } });
            }
            handleCloseModal();
        }
    };
    async function chevronRightClick(idFolder) {
        setDesModalData((prev) => {
            return { ...prev, loading: true };
        });
        const response = await storageService.getDataFolder(idFolder);
        if (response.status === "success") {
            setDesModalData((prev) => {
                return { listFolder: response.data.folder.child_folders, currentFolderName: response.data.folder.name, parentId: response.data.folder.parent_id, selected: idFolder, loading: false };
            });
        } else {
            setDesModalData((prev) => {
                return { ...prev, listFolder: [], loading: false };
            });
            dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Fail to load data!" } });
        }
    }

    async function chevronLeftClick() {
        setDesModalData((prev) => {
            return { ...prev, loading: true };
        });
        const response = await storageService.getDataFolder(desModalData.parentId);
        if (response.status === "success") {
            setDesModalData((prev) => {
                return {
                    listFolder: response.data.folder.child_folders,
                    currentFolderName: response.data.folder.name,
                    parentId: response.data.folder.parent_id,
                    selected: prev.parentId,
                    loading: false,
                };
            });
        } else {
            setDesModalData((prev) => {
                return { ...prev, loading: false };
            });
            dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Fail to load data!" } });
        }
    }
    function selectFolder(idFolder) {
        setDesModalData((prev) => {
            return {
                ...prev,
                selected: idFolder,
            };
        });
    }
    const handleMoveItem = async () => {
        if (storageData.item_selected.type === "folder") {
            const res = await storageService.moveFolder(storageData.item_selected.id, { parent_id: desModalData.selected });
            if (res.status === "success") {
                dispatch({ type: storageActionTypes.activeReloadData });
                setTimeout(() => {
                    dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Move done!" } });
                }, 600);
            } else {
                dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Move fail!" } });
            }
            handleCloseModal();
        } else {
            const res = await storageService.moveFile(storageData.item_selected.id, { parent_id: desModalData.selected });
            if (res.status === "success") {
                dispatch({ type: storageActionTypes.activeReloadData });
                setTimeout(() => {
                    dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Move done!" } });
                }, 600);
            } else {
                dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Move fail!" } });
            }
            handleCloseModal();
        }
    };
    const handleCopyItem = async () => {
        if (storageData.item_selected.type === "folder") {
            const res = await storageService.copyFolder(storageData.item_selected.id, { parent_id: desModalData.selected });
            if (res.status === "success") {
                dispatch({ type: storageActionTypes.activeReloadData });
                setTimeout(() => {
                    dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Copy done!" } });
                }, 600);
            } else {
                dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Copy fail!" } });
            }
            handleCloseModal();
        } else {
            const res = await storageService.copyFile(storageData.item_selected.id, { parent_id: desModalData.selected });
            if (res.status === "success") {
                dispatch({ type: storageActionTypes.activeReloadData });
                setTimeout(() => {
                    dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Copy done!" } });
                }, 600);
            } else {
                dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Copy fail!" } });
            }
            handleCloseModal();
        }
    };
    return (
        <Dialog maxWidth={"xs"} open={open} fullWidth onClose={handleCloseModal} onClick={(e) => e.stopPropagation()} onContextMenu={(e) => e.stopPropagation()} style={{ zIndex: 10000 }}>
            {typeContent === "rename" ? (
                <>
                    <DialogTitle>Rename Folder</DialogTitle>
                    <DialogContent style={{ paddingTop: "20px" }}>
                        <TextField
                            value={folderName}
                            autoFocus
                            label="Folder name"
                            type="text"
                            fullWidth
                            variant="outlined"
                            onChange={(e) => {
                                setFolderName(e.target.value);
                            }}
                        />
                    </DialogContent>
                    <DialogActions>
                        <Button variant="outlined" color="secondary" onClick={handleCloseModal}>
                            Cancel
                        </Button>
                        <Button variant="contained" onClick={handleRenameItem} disabled={folderName === ""}>
                            Rename
                        </Button>
                    </DialogActions>
                </>
            ) : (
                <>
                    <DialogTitle>Select destination</DialogTitle>
                    <DialogContent style={{ paddingTop: "0px" }}>
                        {desModalData.parentId !== "root" ? (
                            <IconButton style={{ border: "1px solid rgb(117 117 117)", marginRight: "10px", width: "35px", height: "35px" }} onClick={chevronLeftClick}>
                                <ChevronLeft />
                            </IconButton>
                        ) : null}
                        <b>{desModalData.currentFolderName}</b>
                        {desModalData.loading ? (
                            <div style={{ height: "200px", display: "flex", justifyContent: "center", alignItems: "center" }}>Loading...</div>
                        ) : (
                            <List style={{ minHeight: "200px" }}>
                                {desModalData.listFolder[0] ? null : <div style={{ height: "200px", display: "flex", justifyContent: "center", alignItems: "center" }}>Select this folder... </div>}
                                {desModalData.listFolder.map((item, index) => {
                                    if (item.folder_id !== storageData.item_selected.id)
                                        return (
                                            <ListItem
                                                key={"itemindex" + index + item.name}
                                                secondaryAction={
                                                    <IconButton edge="end" onClick={() => chevronRightClick(item.folder_id)}>
                                                        <ChevronRight />
                                                    </IconButton>
                                                }
                                                disablePadding
                                            >
                                                <ListItemButton onClick={() => selectFolder(item.folder_id)} selected={desModalData.selected === item.folder_id}>
                                                    <ListItemIcon>
                                                        <Folder />
                                                    </ListItemIcon>
                                                    <ListItemText primary={item.name} />
                                                </ListItemButton>
                                            </ListItem>
                                        );
                                })}
                            </List>
                        )}
                    </DialogContent>
                    <DialogActions>
                        <Button variant="outlined" color="secondary" onClick={handleCloseModal}>
                            Cancel
                        </Button>
                        <Button variant="contained" onClick={typeContent == "copyAction" ? handleCopyItem : handleMoveItem} disabled={desModalData.selected === ""}>
                            Select
                        </Button>
                    </DialogActions>
                </>
            )}
        </Dialog>
    );
}
