import React, { useState } from "react";
import { Divider, Menu, MenuItem } from "@mui/material";
import { useDispatch, useSelector } from "react-redux";
import { storageActionTypes } from "../../../../../redux/User/Storages/storageActionType";
import { Copy, Download, Edit2, FilePlus, FolderPlus, Info, Move, Star, Trash2, RefreshCcw } from "react-feather";
import { Star as MuiStar } from "@material-ui/icons";
import { storageService } from "../../../../../services/User/storages";
import { OPEN_ERROR_ALERT } from "../../../../../redux/User/Alerts/actionTypes";
import { OPEN_SUCCESS_ALERT } from "../../../../../redux/User/Alerts/actionTypes";
import DialogMultiContent from "../DialogMultiContent/DialogMultiContent";

export default function ContextMenu() {
    const dispatch = useDispatch();
    const contextMenuData = useSelector((stores) => stores.Storage.context_menu);
    const itemSelected = useSelector((stores) => stores.Storage.item_selected);

    function handleClose(e) {
        e.stopPropagation();
        dispatch({ type: storageActionTypes.closeContextMenu });
    }
    async function maskAsFavorite() {
        document.getElementById("markItemFavorite").click();
    }
    async function unfavorite() {
        document.getElementById("markItemUnfavorite").click();
    }
    function moveItemActionClick() {
        document.getElementById("moveItemAction").click();
    }
    function copyItemActionClick() {
        document.getElementById("copyItemAction").click();
    }

    function upLoadFileClick() {
        document.getElementById("inputUploadFile").click();
    }
    function upLoadFolderClick() {
        document.getElementById("inputUploadFolder").click();
    }
    function createNewFolderClick() {
        document.getElementById("createNewFolderBtn").click();
    }
    function moveToTrashClick() {
        document.getElementById("moveToTrashAction").click();
    }
    function restoreClick() {
        document.getElementById("restoreAction").click();
    }
    function deleteItemInTrashClick() {
        document.getElementById("deleteAction").click();
    }
    function downloadItemClick() {
        document.getElementById("downloadAction").click();
    }
    function detailItemClick() {
        document.getElementById("viewDetailItem").click();
    }
    return (
        <>
            {contextMenuData.type === "folderOrFile" ? (
                <>
                    {itemSelected.isTrashed ? (
                        <Menu
                            onContextMenu={(e) => {
                                e.preventDefault();
                                e.stopPropagation();
                                dispatch({ type: storageActionTypes.closeContextMenu });
                            }}
                            open={contextMenuData.isOpen}
                            onClose={handleClose}
                            anchorReference="anchorPosition"
                            anchorPosition={{ top: contextMenuData.yAxis, left: contextMenuData.xAxis }}
                        >
                            <MenuItem
                                onClick={(e) => {
                                    restoreClick();
                                    handleClose(e);
                                }}
                                style={{ minWidth: "180px" }}
                            >
                                <RefreshCcw width={17} height={17} style={{ marginRight: "15px" }} /> Restore
                            </MenuItem>
                            <MenuItem
                                onClick={(e) => {
                                    deleteItemInTrashClick();
                                    handleClose(e);
                                }}
                                style={{ minWidth: "180px" }}
                            >
                                <Trash2 width={17} height={17} style={{ marginRight: "15px" }} /> Delete
                            </MenuItem>
                        </Menu>
                    ) : (
                        <>
                            {itemSelected.isOwner ? (
                                <Menu
                                    onContextMenu={(e) => {
                                        e.preventDefault();
                                        e.stopPropagation();
                                        dispatch({ type: storageActionTypes.closeContextMenu });
                                    }}
                                    open={contextMenuData.isOpen}
                                    onClose={handleClose}
                                    anchorReference="anchorPosition"
                                    anchorPosition={{ top: contextMenuData.yAxis, left: contextMenuData.xAxis }}
                                >
                                    {contextMenuData.isFavorite ? (
                                        <MenuItem
                                            onClick={(e) => {
                                                unfavorite();
                                                handleClose(e);
                                            }}
                                            style={{ minWidth: "180px" }}
                                        >
                                            <MuiStar style={{ marginRight: "15px", color: "#ffd500", width: "17px", height: "17px" }} /> Unfavorite
                                        </MenuItem>
                                    ) : (
                                        <MenuItem
                                            onClick={(e) => {
                                                maskAsFavorite();
                                                handleClose(e);
                                            }}
                                            style={{ minWidth: "180px" }}
                                        >
                                            <Star width={17} height={17} style={{ marginRight: "15px" }} /> Favorite
                                        </MenuItem>
                                    )}
                                    <MenuItem
                                        onClick={(e) => {
                                            downloadItemClick();
                                            handleClose(e);
                                        }}
                                        style={{ minWidth: "180px" }}
                                    >
                                        <Download width={17} height={17} style={{ marginRight: "15px" }} /> Download
                                    </MenuItem>
                                    <Divider sx={{ my: 0.5 }} />
                                    <MenuItem
                                        onClick={(e) => {
                                            document.getElementById("renameAction").click();
                                            handleClose(e);
                                        }}
                                        style={{ minWidth: "180px" }}
                                    >
                                        <Edit2 width={17} height={17} style={{ marginRight: "15px" }} /> Rename
                                    </MenuItem>
                                    <MenuItem
                                        onClick={(e) => {
                                            copyItemActionClick();
                                            handleClose(e);
                                        }}
                                        style={{ minWidth: "180px" }}
                                    >
                                        <Copy width={17} height={17} style={{ marginRight: "15px" }} /> Copy
                                    </MenuItem>
                                    <MenuItem
                                        onClick={(e) => {
                                            moveItemActionClick();
                                            handleClose(e);
                                        }}
                                        style={{ minWidth: "180px" }}
                                    >
                                        <Move width={17} height={17} style={{ marginRight: "15px" }} /> Move
                                    </MenuItem>
                                    <Divider sx={{ my: 0.5 }} />
                                    <MenuItem
                                        onClick={(e) => {
                                            detailItemClick();
                                            handleClose(e);
                                        }}
                                        style={{ minWidth: "180px" }}
                                    >
                                        <Info width={17} height={17} style={{ marginRight: "15px" }} /> Detail
                                    </MenuItem>
                                    <MenuItem
                                        onClick={(e) => {
                                            moveToTrashClick();
                                            handleClose(e);
                                        }}
                                        style={{ minWidth: "180px" }}
                                    >
                                        <Trash2 width={17} height={17} style={{ marginRight: "15px" }} /> Move to trash
                                    </MenuItem>
                                </Menu>
                            ) : (
                                <Menu
                                    onContextMenu={(e) => {
                                        e.preventDefault();
                                        e.stopPropagation();
                                        dispatch({ type: storageActionTypes.closeContextMenu });
                                    }}
                                    open={contextMenuData.isOpen}
                                    onClose={handleClose}
                                    anchorReference="anchorPosition"
                                    anchorPosition={{ top: contextMenuData.yAxis, left: contextMenuData.xAxis }}
                                >
                                    <MenuItem
                                        onClick={(e) => {
                                            downloadItemClick();
                                            handleClose(e);
                                        }}
                                        style={{ minWidth: "180px" }}
                                    >
                                        <Download width={17} height={17} style={{ marginRight: "15px" }} /> Download
                                    </MenuItem>
                                    <MenuItem
                                        onClick={(e) => {
                                            detailItemClick();
                                            handleClose(e);
                                        }}
                                        style={{ minWidth: "180px" }}
                                    >
                                        <Info width={17} height={17} style={{ marginRight: "15px" }} /> Detail
                                    </MenuItem>
                                </Menu>
                            )}
                        </>
                    )}
                </>
            ) : (
                <Menu
                    onContextMenu={(e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        dispatch({ type: storageActionTypes.closeContextMenu });
                    }}
                    open={contextMenuData.isOpen}
                    onClose={handleClose}
                    anchorReference="anchorPosition"
                    anchorPosition={{ top: contextMenuData.yAxis, left: contextMenuData.xAxis }}
                >
                    <MenuItem
                        onClick={(e) => {
                            upLoadFileClick();
                            handleClose(e);
                        }}
                        style={{ minWidth: "180px" }}
                    >
                        <FilePlus width={17} height={17} style={{ marginRight: "15px" }} /> Upload new file
                    </MenuItem>
                    <MenuItem
                        onClick={(e) => {
                            upLoadFolderClick();
                            handleClose(e);
                        }}
                        style={{ minWidth: "180px" }}
                    >
                        <FolderPlus width={17} height={17} style={{ marginRight: "15px" }} /> Upload new folder
                    </MenuItem>
                    <Divider sx={{ my: 0.5 }} />
                    <MenuItem
                        onClick={(e) => {
                            createNewFolderClick();
                            handleClose(e);
                        }}
                        style={{ minWidth: "180px" }}
                    >
                        <FolderPlus width={17} height={17} style={{ marginRight: "15px" }} /> Create new folder
                    </MenuItem>
                </Menu>
            )}
        </>
    );
}
