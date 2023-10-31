import { ClickAwayListener, Menu, MenuItem } from "@mui/material";
import React, { useEffect } from "react";
import { useState } from "react";
import { Col, Row } from "react-bootstrap";
import { Copy, Download, Edit2, Info, MoreVertical, Move, Star, Trash2, RefreshCcw } from "react-feather";
import { useDispatch, useSelector } from "react-redux";
import { Card, CardBody } from "reactstrap";
import { imagePath } from "../../../../../constant/imagePath";
import { storageActionTypes } from "../../../../../redux/User/Storages/storageActionType";
import BreadcrumbCt from "../Breadcrumb/BreadcrumbCt";
import CardGridViewMode from "../CardFolder/GirdViewMode/CardGridViewMode";
import CardListViewMode from "../CardFolder/ListViewMode/CardListViewMode";
import ContextMenu from "../ContextMenu/ContextMenu";
import { Star as MuiStar } from "@material-ui/icons";
import { storageService } from "../../../../../services/User/storages";
import { OPEN_SUCCESS_ALERT } from "../../../../../redux/User/Alerts/actionTypes";
import { OPEN_ERROR_ALERT } from "../../../../../redux/User/Alerts/actionTypes";
import DialogMultiContent from "../DialogMultiContent/DialogMultiContent";
import FileSaver from "file-saver";
import DialogDetailFolder from "../DialogMultiContent/DialogDetailFolder";

export default function StoragesData(props) {
    const { onRightClick = true } = props;
    const storageData = useSelector((stores) => stores.Storage);
    const dispatch = useDispatch();
    const [openDialog, setOpenDialog] = useState({ open: false, typeContent: "" });
    const [openDialogDetailFolder, setOpenDialogDetailFolder] = useState({ open: false });
    const [openMoreOptionMenu, setOpenMoreOptionMenu] = useState(false);
    function closeDialog() {
        setOpenDialog({ open: false, typeContent: "" });
    }
    function closeDialogDetailFolder() {
        setOpenDialogDetailFolder({ open: false });
    }
    function clickMoreOption(e) {
        e.stopPropagation();
        setOpenMoreOptionMenu(true);
    }
    function optItemClick(e) {
        e.stopPropagation();
        setOpenMoreOptionMenu(false);
    }
    const handleContextMenu = (event) => {
        event.preventDefault();
        dispatch({
            type: storageActionTypes.openContextMenu,
            payload: {
                item_selected: {},
                context_menu: { isOpen: true, xAxis: event.clientX - 2, yAxis: event.clientY - 4, type: "window" },
            },
        });
    };
    async function maskAsFavorite() {
        if (storageData.item_selected.type === "folder") {
            const res = await storageService.markFavoriteFolder(storageData.item_selected.id);
            if (res.status === "success") {
                dispatch({ type: storageActionTypes.activeReloadData });
                setTimeout(() => {
                    dispatch({ type: storageActionTypes.setItemSelected, payload: { ...storageData.item_selected, isFavorite: true } });
                    dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Mark favorite done!" } });
                }, 600);
            } else {
                dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Mark favorite fail!" } });
            }
        } else {
            const res = await storageService.markFavoriteFile(storageData.item_selected.id);
            if (res.status === "success") {
                dispatch({ type: storageActionTypes.activeReloadData });
                setTimeout(() => {
                    dispatch({ type: storageActionTypes.setItemSelected, payload: { ...storageData.item_selected, isFavorite: true } });
                    dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Mark favorite done!" } });
                }, 600);
            } else {
                dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Mark favorite fail!" } });
            }
        }
    }
    async function unfavorite() {
        if (storageData.item_selected.type === "folder") {
            const res = await storageService.unfavoriteFolder(storageData.item_selected.id);
            if (res.status === "success") {
                dispatch({ type: storageActionTypes.activeReloadData });
                setTimeout(() => {
                    dispatch({ type: storageActionTypes.setItemSelected, payload: { ...storageData.item_selected, isFavorite: false } });
                    dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Unfavorite done!" } });
                }, 600);
            } else {
                dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Have an error occurred! Unfavorite fail!" } });
            }
        } else {
            const res = await storageService.unfavoriteFile(storageData.item_selected.id);
            if (res.status === "success") {
                dispatch({ type: storageActionTypes.activeReloadData });
                setTimeout(() => {
                    dispatch({ type: storageActionTypes.setItemSelected, payload: { ...storageData.item_selected, isFavorite: false } });
                    dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Unfavorite done!" } });
                }, 600);
            } else {
                dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Have an error occurred! Unfavorite fail!" } });
            }
        }
    }
    async function deleteItem() {
        if (storageData.item_selected.type === "folder") {
            const res = await storageService.deleteFolder(storageData.item_selected.id);
            if (res.status === "success") {
                dispatch({ type: storageActionTypes.activeReloadData });
                setTimeout(() => {
                    dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Delete done!" } });
                }, 600);
            } else {
                dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Have an error occurred! Delete fail!" } });
            }
        } else {
            const res = await storageService.deleteFile(storageData.item_selected.id);
            if (res.status === "success") {
                dispatch({ type: storageActionTypes.activeReloadData });
                setTimeout(() => {
                    dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Delete done!" } });
                }, 600);
            } else {
                dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Have an error occurred! Delete fail!" } });
            }
        }
    }
    async function trashItem() {
        if (storageData.item_selected.type === "folder") {
            const res = await storageService.trashFolder(storageData.item_selected.id);
            if (res.status === "success") {
                dispatch({ type: storageActionTypes.activeReloadData });
                setTimeout(() => {
                    dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Move folder to trash done!" } });
                }, 600);
            } else {
                dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Have an error occurred! Action fail!" } });
            }
        } else {
            const res = await storageService.trashFile(storageData.item_selected.id);
            if (res.status === "success") {
                dispatch({ type: storageActionTypes.activeReloadData });
                setTimeout(() => {
                    dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Move file to trash done!" } });
                }, 600);
            } else {
                dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Have an error occurred! Action fail!" } });
            }
        }
    }
    async function untrashItem() {
        if (storageData.item_selected.type === "folder") {
            const res = await storageService.untrashFolder(storageData.item_selected.id);
            if (res.status === "success") {
                dispatch({ type: storageActionTypes.activeReloadData });
                setTimeout(() => {
                    dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Restore done!" } });
                }, 600);
            } else {
                dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Have an error occurred! Action fail!" } });
            }
        } else {
            const res = await storageService.untrashFile(storageData.item_selected.id);
            if (res.status === "success") {
                dispatch({ type: storageActionTypes.activeReloadData });
                setTimeout(() => {
                    dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Restore done!" } });
                }, 600);
            } else {
                dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Have an error occurred! Action fail!" } });
            }
        }
    }
    async function downloadItem() {
        if (storageData.item_selected.type === "folder") {
            const res = await storageService.downloadFolder(storageData.item_selected.id);
            if (res.status === 200) {
                var blob = new Blob([res.data], { type: "application/octet-stream" });
                FileSaver.saveAs(blob, `${storageData.item_selected.name}.zip`);
                setTimeout(() => {
                    dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Download done!" } });
                }, 600);
            } else {
                dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Have an error occurred! Action fail!" } });
            }
        } else {
            const res = await storageService.downloadFile(storageData.item_selected.id);
            if (res.status === 200) {
                var blob = new Blob([res.data], { type: "application/octet-stream" });
                FileSaver.saveAs(blob, `${storageData.item_selected.name}${storageData.item_selected.ext}`);
                setTimeout(() => {
                    dispatch({ type: OPEN_SUCCESS_ALERT, payload: { message: "Download done!" } });
                }, 600);
            } else {
                dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Have an error occurred! Action fail!" } });
            }
        }
    }
    useEffect(() => {
        if (openMoreOptionMenu) setOpenMoreOptionMenu(false); // check MoreOptionMenu co dang mo thi dong=> giam bot render khi no dong san ma selected_item change
        if (storageData.item_selected.id) {
            // check neu dang co selected_item thi lan click vao window tiep theo se huy select_item
            window.onclick = (e) => {
                dispatch({
                    type: storageActionTypes.setItemSelected,
                    payload: {},
                });
            };
        } else {
            window.onclick = null;
        }
    }, [storageData.item_selected.id]);
    useEffect(() => {
        return () => {
            window.onclick = null;
        };
    }, []);
    return (
        <>
            <Card style={{ marginTop: "25px" }} onContextMenu={onRightClick ? handleContextMenu : null}>
                <CardBody style={{ padding: "19px 30px" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", height: "40px" }}>
                        <BreadcrumbCt path={storageData.data?.path || []} />
                        {storageData.item_selected.id ? (
                            <div style={{ position: "relative" }}>
                                {storageData.item_selected.isTrashed ? (
                                    <>
                                        <span id="restoreAction" onClick={untrashItem} className="storage_icon_function">
                                            <RefreshCcw />
                                        </span>
                                        <span id="deleteAction" onClick={deleteItem} className="storage_icon_function">
                                            <Trash2 />
                                        </span>
                                    </>
                                ) : storageData.item_selected.isOwner ? (
                                    <>
                                        <span
                                            id="moveItemAction"
                                            className="storage_icon_function"
                                            title="move"
                                            onClick={(e) => {
                                                setOpenDialog({ open: true, typeContent: "moveAction" });
                                                optItemClick(e);
                                            }}
                                        >
                                            <Move />
                                        </span>
                                        <span
                                            id="downloadAction"
                                            onClick={(e) => {
                                                downloadItem();
                                                optItemClick(e);
                                            }}
                                            title="Download"
                                            className="storage_icon_function"
                                        >
                                            <Download />
                                        </span>
                                        <span id="moveToTrashAction" onClick={trashItem} className="storage_icon_function">
                                            <Trash2 />
                                        </span>
                                        <span className="storage_icon_function" onClick={clickMoreOption}>
                                            <MoreVertical />
                                        </span>
                                        <div className="menu_more_option" style={{ display: openMoreOptionMenu ? "block" : "none" }}>
                                            <div
                                                id="renameAction"
                                                className="opt_item"
                                                onClick={(e) => {
                                                    setOpenDialog({ open: true, typeContent: "rename" });
                                                    optItemClick(e);
                                                }}
                                            >
                                                <Edit2 width={17} height={17} style={{ marginRight: "15px" }} /> Rename
                                            </div>
                                            <div
                                                id="copyItemAction"
                                                className="opt_item"
                                                onClick={(e) => {
                                                    setOpenDialog({ open: true, typeContent: "copyAction" });
                                                    optItemClick(e);
                                                }}
                                            >
                                                <Copy width={17} height={17} style={{ marginRight: "15px" }} /> Copy
                                            </div>
                                            {storageData.item_selected.isFavorite ? (
                                                <div
                                                    className="opt_item"
                                                    id="markItemUnfavorite"
                                                    onClick={(e) => {
                                                        unfavorite();
                                                        optItemClick(e);
                                                    }}
                                                >
                                                    <MuiStar style={{ marginRight: "15px", color: "#ffd500", width: "19px", height: "19px" }} /> Unfavorite
                                                </div>
                                            ) : (
                                                <div
                                                    className="opt_item"
                                                    id="markItemFavorite"
                                                    onClick={(e) => {
                                                        maskAsFavorite();
                                                        optItemClick(e);
                                                    }}
                                                >
                                                    <Star width={17} height={17} style={{ marginRight: "15px" }} /> Favorite
                                                </div>
                                            )}
                                            <div
                                                className="opt_item"
                                                id="viewDetailItem"
                                                onClick={(e) => {
                                                    setOpenDialogDetailFolder({ open: true });
                                                    optItemClick(e);
                                                }}
                                            >
                                                <Info width={17} height={17} style={{ marginRight: "15px" }} /> Detail
                                            </div>
                                        </div>
                                    </>
                                ) : (
                                    <>
                                        <span
                                            id="downloadAction"
                                            onClick={(e) => {
                                                downloadItem();
                                                optItemClick(e);
                                            }}
                                            title="Download"
                                            className="storage_icon_function"
                                        >
                                            <Download />
                                        </span>
                                        <span
                                            id="viewDetailItem"
                                            onClick={(e) => {
                                                setOpenDialogDetailFolder({ open: true });
                                                optItemClick(e);
                                            }}
                                            title="Download"
                                            className="storage_icon_function"
                                        >
                                            <Info />
                                        </span>
                                    </>
                                )}
                            </div>
                        ) : (
                            <></>
                        )}
                    </div>
                    <hr />
                    {storageData.data.child_files[0] == undefined && storageData.data.child_folders[0] == undefined ? (
                        <div style={{ textAlign: "center" }}>
                            <img src={imagePath.EMPTY_FOLDER} alt="" />
                            <div>This folder is empty !!!</div>
                        </div>
                    ) : (
                        <>
                            {storageData.isGridViewMode === true ? (
                                <>
                                    <div style={{ fontWeight: "bold", opacity: "0.5", marginBottom: "23px" }}>FOLDERS</div>
                                    <Row>
                                        {storageData.data.child_folders.map((folder, index) => {
                                            return (
                                                <Col className="col_xll_20p" xl={3} lg={4} md={6} xxl={2} key={"gridviewfolder" + folder.name + index}>
                                                    <CardGridViewMode data={folder} type={"folder"} />
                                                </Col>
                                            );
                                        })}
                                    </Row>
                                    <div style={{ fontWeight: "bold", opacity: "0.5", marginBottom: "23px" }}>FILES</div>
                                    <Row>
                                        {storageData.data.child_files.map((file, index) => {
                                            return (
                                                <Col className="col_xll_20p" xl={3} lg={4} md={6} xxl={2} key={"gridviewfile" + file.name + index}>
                                                    <CardGridViewMode data={file} type={"file"} />
                                                </Col>
                                            );
                                        })}
                                    </Row>
                                </>
                            ) : (
                                <div style={{ overflow: "auto" }}>
                                    <Row className="head_table" style={{ minWidth: "1000px" }}>
                                        <Col xs={6}>
                                            <span>Name</span>
                                        </Col>
                                        <Col xs={2}>
                                            <span>Owner</span>
                                        </Col>
                                        <Col xs={2}>
                                            <span>Last Edited</span>
                                        </Col>
                                        <Col xs={2}>
                                            <span>Size</span>
                                        </Col>
                                    </Row>
                                    {storageData.data.child_folders.map((folder, index) => {
                                        return <CardListViewMode data={folder} type={"folder"} key={"listviewItemfolder" + folder.name + index} />;
                                    })}
                                    {storageData.data.child_files.map((file, index) => {
                                        return <CardListViewMode data={file} type={"file"} key={"listviewItemfile" + file.name + index} />;
                                    })}
                                </div>
                            )}
                        </>
                    )}
                    <ContextMenu />
                </CardBody>
            </Card>
            <DialogMultiContent open={openDialog.open} handleCloseModal={closeDialog} typeContent={openDialog.typeContent} />
            <DialogDetailFolder open={openDialogDetailFolder.open} handleCloseModal={closeDialogDetailFolder} />
        </>
    );
}
