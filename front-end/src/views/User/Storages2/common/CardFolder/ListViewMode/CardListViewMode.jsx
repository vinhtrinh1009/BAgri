import React from "react";
import { Folder, Star } from "@material-ui/icons";
import { Col, Row } from "react-bootstrap";
import { imagePath } from "../../../../../../constant/imagePath";
import { exchangeSizeValue } from "../../../../../../utils/commonFunction";
import { useDispatch, useSelector } from "react-redux";
import { storageActionTypes } from "../../../../../../redux/User/Storages/storageActionType";
import { useNavigate } from "react-router";
import { IPFS_URL } from "src/constant/config";

export default function CardListViewMode(props) {
    const { data, type } = props;
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const selectedItem = useSelector((stores) => stores.Storage.item_selected);
    const userId = useSelector((stores) => stores.User.user.user_id);
    const handleContextMenu = (event) => {
        event.preventDefault();
        event.stopPropagation();
        dispatch({
            type: storageActionTypes.openContextMenu,
            payload: {
                item_selected: {
                    id: data.folder_id || data.file_id,
                    isFavorite: data.labels.favorited,
                    isTrashed: data.labels.trashed,
                    isOwner: data.owner.user_id === userId,
                    name: data.name,
                    ext: data.ext_name || ".zip",
                    type: type,
                },
                context_menu: { isOpen: true, xAxis: event.clientX - 2, yAxis: event.clientY - 4, type: "folderOrFile", isFavorite: data.labels.favorited },
            },
        });
    };
    function selectItem(e) {
        e.stopPropagation();
        dispatch({
            type: storageActionTypes.setItemSelected,
            payload: {
                id: data.folder_id || data.file_id,
                isFavorite: data.labels.favorited,
                isTrashed: data.labels.trashed,
                isOwner: data.owner.user_id === userId,
                name: data.name,
                ext: data.ext_name || ".zip",
                type: type,
            },
        });
    }
    function dbclickGoDetail() {
        if (data.owner.user_id === userId) {
            navigate(`/storages/${data.folder_id}`);
        } else {
            navigate(`/storages/platform-artifact/${data.folder_id}`);
        }
    }

    function dbclickGoView() {
        if (data.cid) {
            window.open(IPFS_URL + "/" + data.cid, "_blank");
        }
    }

    return (
        <Row
            className={`card_list_view_mode card_mouse_envent  ${selectedItem.id === (data.folder_id || data.file_id) ? "activeItem" : ""}`}
            onClick={selectItem}
            onDoubleClick={type === "folder" ? dbclickGoDetail : dbclickGoView}
            onContextMenu={handleContextMenu}
            style={{ cursor: "context-menu", minWidth: "1000px" }}
        >
            <Col xs={6} className="card_list_view_mode_name">
                <span className="card_list_view_mode_icon">{type === "folder" ? <Folder /> : <img src={imagePath[data.ext_name] || imagePath.UNKNOW} width={30} height={30} alt="" />}</span>
                <span style={{ fontWeight: "bold" }}>
                    {data?.name || "Unknow"}
                    {type === "file" ? data.ext_name : ""}
                </span>
            </Col>
            <Col xs={2}>
                <span className="card_list_view_mode_data">{data?.owner?.username || "---"}</span>
            </Col>
            <Col xs={2}>
                <span className="card_list_view_mode_data">2021 - 10 - 20</span>
            </Col>
            <Col xs={2} style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <span className="card_list_view_mode_data">{type === "file" ? exchangeSizeValue(data.size) : "---"}</span>
                <span className="sub_icon" style={{ float: "right", color: "#ffd500" }} title="favorite">
                    {data.labels.favorited ? <Star width={8} height={8} /> : <></>}
                </span>
            </Col>
        </Row>
    );
}
