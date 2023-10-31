import React, { useEffect } from "react";
import { Button } from "@mui/material";
import { FC, useMemo, CSSProperties } from "react";
import { EdgeProps, getMarkerEnd, useStoreState, getBezierPath, getSmoothStepPath, getEdgeCenter, ArrowHeadType } from "react-flow-renderer";
import { getEdgeParams } from "./utils";
import { Edit2, Trash2 } from "react-feather";
import ClickAwayListener from "@mui/material/ClickAwayListener";
import { useSelector, useDispatch } from "react-redux";
import { STEP2_RELATIONSHIPS } from "src/redux/User/DApps/actionTypes";
import { relationShipType } from "../../../../../../constant/relationShipType";

export default function FloatingEdge({ id, source, target, arrowHeadType = ArrowHeadType.Arrow, markerEndId, style, data }) {
    const selected = useSelector((state) => state.DApp.selected);
    const step2Relationships = useSelector((state) => state.DApp.step2Relationships);
    const dispatch = useDispatch();
    const [open, setOpen] = React.useState(false);
    useEffect(() => {
        if (open == true) {
            document.querySelector(".react-flow__nodes").style.zIndex = 0;
        } else {
            document.querySelector(".react-flow__nodes").style.zIndex = 3;
        }
    }, [open]);
    const handleClick = () => {
        setOpen((prev) => !prev);
    };

    const handleClickAway = () => {
        setOpen(false);
    };

    function changeRelationShip(newType) {
        const newRelationShip = step2Relationships.map((rel, index) => {
            if (rel.id === id) {
                return {
                    ...rel,
                    id: rel.source + "-" + newType + "-" + rel.target,
                    data: {
                        ...rel.data,
                        id: rel.source + "-" + newType + "-" + rel.target,
                        type: newType,
                    },
                };
            }
            return rel;
        });
        dispatch({ type: STEP2_RELATIONSHIPS, payload: newRelationShip });
    }
    function removeRelationship() {
        document.querySelector(".react-flow__nodes").style.zIndex = 3;
        const newRelationShip = step2Relationships.filter((rel, index) => rel.id !== id);
        dispatch({ type: STEP2_RELATIONSHIPS, payload: newRelationShip });
    }

    function getArrowMaker() {
        if (data.type == relationShipType.OneToOne) {
            return {
                textbtn: "One - to - One",
                makerStart: "",
                makerEnd: "",
            };
        }
        if (data.type == relationShipType.OneToMany) {
            return {
                textbtn: "One - to - Many",
                makerStart: "",
                makerEnd: "url(#react-flow__arrow_end_many)",
            };
        }
        if (data.type == relationShipType.ManyToOne) {
            return {
                textbtn: "Many - to - One",
                makerStart: "url(#react-flow__arrow_start_many)",
                makerEnd: "",
            };
        }
        if (data.type == relationShipType.ManyToMany) {
            return {
                textbtn: "Many - to - Many",
                makerStart: "url(#react-flow__arrow_start_many)",
                makerEnd: "url(#react-flow__arrow_end_many)",
            };
        }
        return {
            textbtn: "One - to - One",
            makerStart: "",
            makerEnd: "",
        };
    }

    const nodes = useStoreState((state) => state.nodes);
    // const markerEnd = getMarkerEnd(arrowHeadType, markerEndId);
    const { makerStart, makerEnd, textbtn } = getArrowMaker();

    const sourceNode = useMemo(() => nodes.find((n) => n.id === source), [source, nodes]);
    const targetNode = useMemo(() => nodes.find((n) => n.id === target), [target, nodes]);

    if (!sourceNode || !targetNode) {
        return null;
    }

    const { sx, sy, tx, ty, sourcePos, targetPos } = getEdgeParams(sourceNode, targetNode);

    const d = getBezierPath({
        sourceX: sx,
        sourceY: sy,
        sourcePosition: sourcePos,
        targetPosition: targetPos,
        targetX: tx,
        targetY: ty,
    });
    const smoothPath = getSmoothStepPath({
        sourceX: sx,
        sourceY: sy,
        sourcePosition: sourcePos,
        targetPosition: targetPos,
        targetX: tx,
        targetY: ty,
        borderRadius: 0,
    });

    const [edgeCenterX, edgeCenterY] = getEdgeCenter({
        sourceX: sx,
        sourceY: sy,
        targetX: tx,
        targetY: ty,
    });
    let foreignObjectSize = {
        width: 112,
        height: 29,
    };

    return (
        <>
            <marker className="react-flow__arrowhead" id="react-flow__arrow_start_many" markerWidth="41.5" markerHeight="37.5" viewBox="-10 -10 20 20" orient="auto" refX="-5" refY="0">
                <polyline stroke={open ? "#4498ed" : "#B1B1B1"} strokeLinecap="round" strokeLinejoin="round" strokeWidth="0.8px" fill="none" points="-5,-3 0,0 -5,3"></polyline>
            </marker>
            <marker className="react-flow__arrowhead" id="react-flow__arrow_end_many" markerWidth="41.5" markerHeight="37.5" viewBox="-10 -10 20 20" orient="auto" refX="5" refY="0">
                <polyline stroke={open ? "#4498ed" : "#B1B1B1"} strokeLinecap="round" strokeLinejoin="round" strokeWidth="0.8px" fill="none" points="5,3 0,0 5,-3"></polyline>
            </marker>
            <path id={id} className={"react-flow__edge-path"} d={smoothPath} markerStart={makerStart} markerEnd={makerEnd} style={{ ...style, strokeWidth: open ? "1.5px" : "1px" }} />
            {id.includes(selected) && !data.is_old_data ? (
                <foreignObject
                    style={{ zIndex: "111", overflow: "visible" }}
                    className="icon_function"
                    x={edgeCenterX - foreignObjectSize.width / 2}
                    y={edgeCenterY - foreignObjectSize.height / 2}
                    requiredExtensions="http://www.w3.org/1999/xhtml"
                >
                    <ClickAwayListener onClickAway={handleClickAway}>
                        <div style={{ position: "relative" }} className="btn_click_away">
                            <span onClick={handleClick} className="icon_btn_click" style={{ width: "max-content", height: "29px", padding: "5px", fontSize: "13px" }}>
                                <i style={{ marginRight: "10px", width: "max-content" }}>{textbtn}</i>
                                <Edit2 style={{ width: "14px", height: "14px" }} />
                            </span>
                            {open ? (
                                <div className="multichoice_type_edge">
                                    <div onClick={() => changeRelationShip(relationShipType.OneToOne)}>One-to-One</div>
                                    <div onClick={() => changeRelationShip(relationShipType.OneToMany)}>One-to-Many</div>
                                    <div onClick={() => changeRelationShip(relationShipType.ManyToOne)}>Many-to-One</div>
                                    <div onClick={() => changeRelationShip(relationShipType.ManyToMany)}>Many-to-Many</div>
                                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", borderTop: "1px solid #B6C6D1", cursor: "default" }}>
                                        Relationships{" "}
                                        <span style={{ width: "29px", height: "29px", cursor: "pointer" }} onClick={removeRelationship}>
                                            <Trash2 />
                                        </span>
                                    </div>
                                </div>
                            ) : null}
                        </div>
                    </ClickAwayListener>
                </foreignObject>
            ) : null}
        </>
    );
}
