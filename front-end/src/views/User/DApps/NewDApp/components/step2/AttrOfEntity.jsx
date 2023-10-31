import React, { useRef, useState } from "react";
import { Security } from "@material-ui/icons";
import { MoreHorizontal, Trash2 } from "react-feather";
import { useDispatch, useSelector } from "react-redux";
import { SELECTED_NODE, STEP2_ENTITIES, STEP2_RELATIONSHIPS } from "src/redux/User/DApps/actionTypes";
import { Snackbar } from "@mui/material";
import MuiAlert from "@mui/material/Alert";
import { checkNameAttrUnique } from "./utils";
import { invalidNameAttr } from "../../../../../../constant/invalidNameAttr";

export default function AttrOfEntity(props) {
    const { attr, isPrimaryKey, entityId, entityListAttr } = props;
    const dispatch = useDispatch();
    const step2Entities = useSelector((state) => state.DApp.step2Entities);
    const [openCommentBox, setOpenCommentBox] = useState(false);
    const [openAlert, setOpenAlert] = React.useState({
        open: false,
        type: "error",
        message: "",
    });
    const [storeName, setStoreName] = React.useState("");

    const handleClose = (event, reason) => {
        if (reason === "clickaway") {
            return;
        }
        setOpenAlert((prev) => {
            return {
                ...prev,
                open: false,
            };
        });
    };
    function changeNameAttr(newName) {
        const newStep2Entities = step2Entities.map((enti, index) => {
            if (enti.id === entityId) {
                return {
                    ...enti,
                    data: {
                        ...enti.data,
                        attributes: enti.data.attributes.map((attrVal, i) => {
                            if (attrVal.idAttr === attr.idAttr) {
                                return {
                                    ...attrVal,
                                    name: newName,
                                };
                            }
                            return attrVal;
                        }),
                    },
                };
            }
            return enti;
        });
        dispatch({ type: STEP2_ENTITIES, payload: newStep2Entities });
    }
    function onInputNameFocus(event) {
        setStoreName(event.target.value);
    }
    function checkNameOnlyLetterNumberLetterFisrt(name) {
        if (!/[^a-z0-9_]+/g.test(name)) {
            if (isNaN(name[0])) {
                return true;
            }
        }
        return false;
    }
    function onInputNameBlur() {
        let currentInputName = attr.name.trim();
        if (currentInputName == "") {
            changeNameAttr(storeName);
        } else if (currentInputName.includes(" ")) {
            setOpenAlert({
                open: true,
                type: "error",
                message: `${currentInputName} is not valid! (It must be no space)`,
            });
            changeNameAttr(storeName);
        } else if (checkNameAttrUnique(entityListAttr, entityListAttr.length, currentInputName, attr.idAttr) === false) {
            setOpenAlert({
                open: true,
                type: "error",
                message: `${currentInputName} already exists!`,
            });
            changeNameAttr(storeName);
        } else if (invalidNameAttr[currentInputName] !== undefined) {
            setOpenAlert({
                open: true,
                type: "error",
                message: `${currentInputName} is keyword. Not allowed!`,
            });
            changeNameAttr(storeName);
        } else if (!checkNameOnlyLetterNumberLetterFisrt(currentInputName)) {
            setOpenAlert({
                open: true,
                type: "error",
                message: `${currentInputName} is not valid! Only letter and number. Letter beginning`,
            });
            changeNameAttr(storeName);
        } else {
            changeNameAttr(currentInputName);
        }
    }

    function changePrimaryKey(attrId) {
        const newStep2Entities = step2Entities.map((enti, index) => {
            if (enti.id === entityId) {
                return {
                    ...enti,
                    data: {
                        ...enti.data,
                        attributes: enti.data.attributes.map((attrVal, i) => {
                            if (attrVal.idAttr === attr.idAttr) {
                                return {
                                    ...attrVal,
                                    encrypt: false,
                                };
                            }
                            return attrVal;
                        }),
                        primary_key: attrId,
                    },
                };
            }
            return enti;
        });
        dispatch({ type: STEP2_ENTITIES, payload: newStep2Entities });
    }
    function setEncrypt(bool) {
        if (bool == true && isPrimaryKey) {
            setOpenAlert({
                open: true,
                type: "error",
                message: "Can not encrypt primary key attribute!",
            });
        } else {
            const newStep2Entities = step2Entities.map((enti, index) => {
                if (enti.id === entityId) {
                    return {
                        ...enti,
                        data: {
                            ...enti.data,
                            attributes: enti.data.attributes.map((attrVal, i) => {
                                if (attrVal.idAttr === attr.idAttr) {
                                    return {
                                        ...attrVal,
                                        encrypt: bool,
                                    };
                                }
                                return attrVal;
                            }),
                        },
                    };
                }
                return enti;
            });
            dispatch({ type: STEP2_ENTITIES, payload: newStep2Entities });
        }
    }

    function updateNameAttr(event) {
        changeNameAttr(event.target.value);
    }
    function updateDescriptionAttr(event) {
        const newStep2Entities = step2Entities.map((enti, index) => {
            if (enti.id === entityId) {
                return {
                    ...enti,
                    data: {
                        ...enti.data,
                        attributes: enti.data.attributes.map((attrVal, i) => {
                            if (attrVal.idAttr === attr.idAttr) {
                                return {
                                    ...attrVal,
                                    description: event.target.value,
                                };
                            }
                            return attrVal;
                        }),
                    },
                };
            }
            return enti;
        });
        dispatch({ type: STEP2_ENTITIES, payload: newStep2Entities });
    }
    function removeAttr() {
        if (isPrimaryKey) {
            setOpenAlert({
                open: true,
                type: "error",
                message: "Can not remove primary key attribute!",
            });
        } else {
            const newStep2Entities = step2Entities.map((enti, index) => {
                if (enti.id === entityId) {
                    return {
                        ...enti,
                        data: {
                            ...enti.data,
                            attributes: enti.data.attributes.filter((attrVal, i) => attrVal.idAttr !== attr.idAttr),
                        },
                    };
                }
                return enti;
            });
            dispatch({ type: STEP2_ENTITIES, payload: newStep2Entities });
        }
    }
    function changeTypeOfAttr(event) {
        const newStep2Entities = step2Entities.map((enti, index) => {
            if (enti.id === entityId) {
                return {
                    ...enti,
                    data: {
                        ...enti.data,
                        attributes: enti.data.attributes.map((attrVal, i) => {
                            if (attrVal.idAttr === attr.idAttr) {
                                return {
                                    ...attrVal,
                                    type: event.target.value,
                                };
                            }
                            return attrVal;
                        }),
                    },
                };
            }
            return enti;
        });
        dispatch({ type: STEP2_ENTITIES, payload: newStep2Entities });
    }
    function toggleCommentBox(show) {
        setOpenCommentBox(show);
    }

    return (
        <>
            <div className="rowdata">
                <input type="text" value={attr.name} onChange={updateNameAttr} onBlur={onInputNameBlur} onFocus={onInputNameFocus} />
                <select className="type_select" onChange={changeTypeOfAttr} defaultValue={attr.type}>
                    <option value="string">string</option>
                    <option value="file">file</option>
                </select>

                <span className="icon_function">
                    <span className={isPrimaryKey ? "primary_key" : ""} onClick={() => changePrimaryKey(attr.idAttr)}>
                        <i className="fa fa-key"></i>
                    </span>
                    <span className={attr.encrypt ? "encrypt" : ""} onClick={() => setEncrypt(!attr.encrypt)}>
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            aria-hidden="true"
                            focusable="false"
                            data-prefix="fas"
                            data-icon="shield-alt"
                            className="svg-inline--fa fa-shield-alt fa-w-16"
                            role="img"
                            viewBox="0 0 512 512"
                        >
                            <path
                                fill="currentColor"
                                d="M466.5 83.7l-192-80a48.15 48.15 0 0 0-36.9 0l-192 80C27.7 91.1 16 108.6 16 128c0 198.5 114.5 335.7 221.5 380.3 11.8 4.9 25.1 4.9 36.9 0C360.1 472.6 496 349.3 496 128c0-19.4-11.7-36.9-29.5-44.3zM256.1 446.3l-.1-381 175.9 73.3c-3.3 151.4-82.1 261.1-175.8 307.7z"
                            />
                        </svg>
                    </span>
                    <span onClick={() => toggleCommentBox(true)} className={openCommentBox ? "primary_key the_comment" : "the_comment"}>
                        <MoreHorizontal />
                    </span>
                    <div className="comment_box" style={{ display: openCommentBox ? "block" : "none" }}>
                        <div className="close_comment_box" onClick={() => toggleCommentBox(false)}></div>
                        <div className="comment_box_content">
                            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "5px" }}>
                                <div>Comment</div>
                                <span onClick={removeAttr}>
                                    <Trash2 />
                                </span>
                            </div>
                            <textarea className="input_comment" name="comment" defaultValue={attr.description} onChange={updateDescriptionAttr}></textarea>
                        </div>
                    </div>
                </span>
            </div>
            <Snackbar anchorOrigin={{ vertical: "top", horizontal: "center" }} open={openAlert.open} autoHideDuration={4000} onClose={handleClose} style={{ zIndex: "10000", top: "90px" }}>
                <MuiAlert elevation={6} onClose={handleClose} severity={openAlert.type} variant="filled">
                    {openAlert.message}
                </MuiAlert>
            </Snackbar>
        </>
    );
}
