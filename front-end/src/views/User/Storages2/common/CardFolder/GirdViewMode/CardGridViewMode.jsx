import { Folder, Star } from "@material-ui/icons";
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router";
import { imagePath } from "../../../../../../constant/imagePath";
import { storageActionTypes } from "../../../../../../redux/User/Storages/storageActionType";
import { exchangeSizeValue } from "../../../../../../utils/commonFunction";
import { IPFS_URL } from "src/constant/config";

export default function CardGridViewMode(props) {
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
            window.open( IPFS_URL + "/" + data.cid, "_blank");
        }
    }

    return (
        <div
            className={`card_grid_view_mode card_mouse_envent ${selectedItem.id === (data.folder_id || data.file_id) ? "activeItem" : ""}`}
            onClick={selectItem}
            onDoubleClick={type === "folder" ? dbclickGoDetail : dbclickGoView}
            onContextMenu={handleContextMenu}
            style={{ cursor: "context-menu" }}
        >
            <span className="card_grid_view_mode_icon">{type === "folder" ? <Folder /> : <img src={imagePath[data.ext_name] || imagePath.UNKNOW} width={30} height={30} alt="" />}</span>
            <div className="card_grid_view_mode_title">
                <div style={{ fontWeight: "bold" }}>
                    {data?.name || "Unknow"}
                    {type === "file" ? data.ext_name : ""}
                </div>
                {type === "file" ? <div style={{ font: "12px/14px Roboto", opacity: "0.65" }}>{exchangeSizeValue(data.size)}</div> : null}
                <span className="sub_icon" title="favorite">
                    {data.labels.favorited ? <Star width={12} height={12} /> : <></>}
                </span>
            </div>
        </div>
    );
}
