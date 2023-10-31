import React, { useRef, useState } from "react";
import { SELECTED_NODE, STEP2_ENTITIES, STEP2_RELATIONSHIPS } from "src/redux/User/DApps/actionTypes";
import { ArrowRight, ColorLens } from "@material-ui/icons";
import { Edit3, Trash2, MoreHorizontal } from "react-feather";
import { useDispatch, useSelector } from "react-redux";
import { Button } from "@mui/material";
import { colors } from "../../NewDApp/components/step2/const";
import AttrOfEntity from "./AttrOfEntity";
import { v4 as uuidv4 } from "uuid";
import { checkNameAttrUnique, checkNameEntityUnique } from "../../NewDApp/components/step2/utils";
import { Snackbar } from "@mui/material";
import MuiAlert from "@mui/material/Alert";
import { OPEN_ERROR_ALERT } from "src/redux/User/Alerts/actionTypes";

export default function AccordionEntity(props) {
    const { entity } = props;
    const dispatch = useDispatch();
    const [openCommentBox, setOpenCommentBox] = useState(false);
    const [isChangeNameEntity, setIsChangeNameEntity] = useState(false);
    const step2Entities = useSelector((state) => state.DApp.step2Entities);
    const step2Relationships = useSelector((state) => state.DApp.step2Relationships);
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
    function changeNameEntity(newName) {
        const newStep2Entities = step2Entities.map((enti, index) => {
            if (enti.id === entity.id) {
                return {
                    ...enti,
                    data: {
                        ...enti.data,
                        name: newName,
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
        let currentInputName = entity.data.name.trim();
        if (currentInputName == "") {
            changeNameEntity(storeName);
        } else if (currentInputName.includes(" ")) {
            setOpenAlert({
                open: true,
                type: "error",
                message: `${currentInputName} is not valid! (It must be no space)`,
            });
            // dispatch({ type: OPEN_ERROR_ALERT, payload: { message: `${currentInputName} is not valid! (It must be no space)` } });
            changeNameEntity(storeName);
        } else if (checkNameEntityUnique(step2Entities, step2Entities.length, currentInputName, entity.id) == false) {
            setOpenAlert({
                open: true,
                type: "error",
                message: `${currentInputName} already exists!`,
            });
            // dispatch({ type: OPEN_ERROR_ALERT, payload: { message: `${currentInputName} already exists!` } });

            changeNameEntity(storeName);
        } else if (!checkNameOnlyLetterNumberLetterFisrt(currentInputName)) {
            setOpenAlert({
                open: true,
                type: "error",
                message: `${currentInputName} is not valid! Only letter and number. Letter beginning`,
            });
            changeNameEntity(storeName);
        } else {
            changeNameEntity(currentInputName);
        }
        setIsChangeNameEntity(false);
    }
    function changeColorEntity(colorChange) {
        const newStep2Entities = step2Entities.map((enti, index) => {
            if (enti.id === entity.id) {
                return {
                    ...entity,
                    data: {
                        ...entity.data,
                        color: colorChange,
                    },
                };
            }
            return enti;
        });
        dispatch({ type: STEP2_ENTITIES, payload: newStep2Entities });
    }
    function addAttr() {
        const numberAttrOfEntiy = entity.data.attributes.length;
        let indexNameAttr = numberAttrOfEntiy;
        while (checkNameAttrUnique(entity.data.attributes, numberAttrOfEntiy, "attribute_" + indexNameAttr, "#") == false) {
            indexNameAttr = indexNameAttr + 1;
        }
        const newAttr = {
            name: "attribute_" + indexNameAttr,
            type: "string",
            encrypt: false,
            description: "",
            idAttr: uuidv4(),
        };
        const newStep2Entities = step2Entities.map((enti, index) => {
            if (enti.id === entity.id) {
                return {
                    ...entity,
                    data: {
                        ...entity.data,
                        attributes: [...entity.data.attributes, newAttr],
                    },
                };
            }
            return enti;
        });
        dispatch({ type: STEP2_ENTITIES, payload: newStep2Entities });
    }
    function updateNameEntity(event) {
        changeNameEntity(event.target.value);
    }
    function updateDescriptionEntity(event) {
        const newStep2Entities = step2Entities.map((enti, index) => {
            if (enti.id === entity.id) {
                return {
                    ...enti,
                    data: {
                        ...enti.data,
                        description: event.target.value,
                    },
                };
            }
            return enti;
        });
        dispatch({ type: STEP2_ENTITIES, payload: newStep2Entities });
    }
    function clearDescriptionEntity(event) {
        const newStep2Entities = step2Entities.map((enti, index) => {
            if (enti.id === entity.id) {
                return {
                    ...enti,
                    data: {
                        ...enti.data,
                        description: "",
                    },
                };
            }
            return enti;
        });
        dispatch({ type: STEP2_ENTITIES, payload: newStep2Entities });
    }
    function removeEntity() {
        const newStep2Entities = step2Entities.filter((enti, index) => enti.id !== entity.id);
        dispatch({ type: STEP2_ENTITIES, payload: newStep2Entities });
        const newRelationShip = step2Relationships.filter((rel, index) => rel.id.includes(entity.id) === false);
        dispatch({ type: STEP2_RELATIONSHIPS, payload: newRelationShip });
    }
    function clickOnEntity() {
        dispatch({ type: SELECTED_NODE, payload: entity.id });
    }
    function onKeyEnterDown(e) {
        if (e.key == "Enter") {
            onInputNameBlur();
            // setIsChangeNameEntity(false);
        }
    }
    function toggleCommentBox(show) {
        setOpenCommentBox(show);
    }
    return (
        <div className="dapp_accordion" style={{ borderLeft: "6px solid " + entity.data.color }}>
            <input type="radio" name="listEntities" id={`${entity.id}-header`} style={{ display: "none" }} />
            <label className="accordion_summary" htmlFor={`${entity.id}-header`} onClick={clickOnEntity}>
                <span className="accordion_summary_title">
                    <span>
                        <ArrowRight />
                    </span>
                    {isChangeNameEntity ? (
                        <span className="input_intity_name">
                            <input type="text" value={entity.data.name} onChange={updateNameEntity} onFocus={onInputNameFocus} onBlur={onInputNameBlur} onKeyDown={onKeyEnterDown} />
                        </span>
                    ) : (
                        <span>{entity.data.name}</span>
                    )}
                </span>
                <span className="icon_function">
                    {entity.data.is_old_data ? (
                        <></>
                    ) : (
                        <>
                            <span onClick={() => setIsChangeNameEntity(true)}>
                                <Edit3 />
                            </span>
                            <span onClick={removeEntity}>
                                <Trash2 />
                            </span>
                        </>
                    )}

                    <span onClick={() => toggleCommentBox(true)} className={openCommentBox ? "primary_key the_comment" : "the_comment"}>
                        <MoreHorizontal />
                    </span>
                    <div className="comment_box" style={{ display: openCommentBox ? "block" : "none" }}>
                        <div className="close_comment_box" onClick={() => toggleCommentBox(false)}></div>
                        <div className="comment_box_content">
                            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "5px" }}>
                                <div>Comment</div>
                                <span onClick={clearDescriptionEntity}>
                                    <Trash2 />
                                </span>
                            </div>
                            <textarea className="input_comment" name="comment" value={entity.data.description} onChange={updateDescriptionEntity}></textarea>
                        </div>
                    </div>
                </span>
            </label>
            <div className="accordion_content" style={{ "--attrlength": entity?.data.attributes.length || 0 }}>
                {entity.data.attributes.map((attr, j) => {
                    return <AttrOfEntity key={attr.idAttr} attr={attr} isPrimaryKey={attr.idAttr === entity.data.primary_key} entityId={entity.id} entityListAttr={entity.data.attributes} />;
                })}
                <div className="accordion_footer">
                    <label htmlFor={`multichoice_colors_${entity.id}`} className="multichoice_colors">
                        <ColorLens />
                        <input className="multi_colors" style={{ display: "none" }} type="checkbox" id={`multichoice_colors_${entity.id}`} />
                        <div className="colors">
                            {colors.map((color, i) => {
                                return <div key={color + entity.id} style={{ background: color }} onClick={() => changeColorEntity(color)}></div>;
                            })}
                        </div>
                    </label>
                    <Button variant="outlined" style={{ margin: "11px", textTransform: "capitalize" }} onClick={addAttr}>
                        Add Attribute
                    </Button>
                </div>
            </div>
            <Snackbar anchorOrigin={{ vertical: "top", horizontal: "center" }} open={openAlert.open} autoHideDuration={4000} onClose={handleClose} style={{ zIndex: "10000", top: "90px" }}>
                <MuiAlert elevation={6} onClose={handleClose} severity={openAlert.type} variant="filled">
                    {openAlert.message}
                </MuiAlert>
            </Snackbar>
        </div>
    );
}
