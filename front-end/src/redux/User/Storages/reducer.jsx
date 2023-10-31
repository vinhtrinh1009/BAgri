import { storageActionTypes } from "./storageActionType";

const initial_state = {
    data: {
        child_files: [],
        child_folders: [],
        folder_id: "",
        labels: { favorited: false, trashed: false, restricted: false, viewed: false },
        name: "",
        owner: { user_id: "", username: "", full_name: "" },
        parent_id: "root",
        path: [],
        shared: [],
        total_size: 0,
        type: "MY_STORAGE_ROOT",
    },
    reload_data_storage: false,
    item_selected: {},
    context_menu: { isOpen: false, xAxis: 0, yAxis: 0, type: "folderOrFile", isFavorite: false },
    isGridViewMode: true,
    loading: false,
};

export default (state = initial_state, action) => {
    switch (action.type) {
        case storageActionTypes.activeReloadData:
            return { ...state, reload_data_storage: !state.reload_data_storage };
        case storageActionTypes.openContextMenu:
            return { ...state, ...action.payload };
        case storageActionTypes.closeContextMenu:
            return { ...state, context_menu: { ...state.context_menu, isOpen: false } };
        case storageActionTypes.setItemSelected:
            return { ...state, item_selected: action.payload };
        case storageActionTypes.toggleViewMode:
            return { ...state, isGridViewMode: !state.isGridViewMode };
        case storageActionTypes.setStorageData:
            return { ...state, data: { ...state.data, ...action.payload }, loading: false };
        default:
            return { ...state };
    }
};
export const storageActions = {
    // updatePopupDetail: (body) => ({ type: storageActionTypes.updatePopupDetail, payload: body }),
};
