import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { Button } from "@material-ui/core";
import { Plus, ChevronLeft } from "react-feather";
import { colors, initialAttribute, initialNode, initialEntity } from "../../NewDApp/components/step2/const";
import { SELECTED_NODE, STEP2_ENTITIES, STEP2_RELATIONSHIPS } from "src/redux/User/DApps/actionTypes";
import AccordionEntity from "./AccordionEntity";
import { v4 as uuidv4 } from "uuid";
import { checkNameEntityUnique } from "../../NewDApp/components/step2/utils";

export default function Step2Sidebar() {
    const dispatch = useDispatch();
    const step2Entities = useSelector((state) => state.DApp.step2Entities);
    function addEntity() {
        const newEntityIndex = step2Entities.length;
        let newEntityNameIndex = newEntityIndex || 1;
        while (checkNameEntityUnique(step2Entities, newEntityIndex, "entity_" + newEntityNameIndex, "#") === false) {
            newEntityNameIndex = newEntityNameIndex + 1;
        }
        const id_Entity = uuidv4();
        const firstIdAttr = uuidv4();
        dispatch({
            type: STEP2_ENTITIES,
            payload: [
                ...step2Entities,
                {
                    ...initialNode,
                    id: id_Entity,
                    position: {
                        ...initialNode.position,
                        x: Math.floor(Math.random() * 600),
                        y: Math.floor(Math.random() * 400),
                    },
                    data: {
                        ...initialNode.data,
                        name: "entity_" + newEntityNameIndex,
                        attributes: [{ ...initialAttribute, name: "attribute_1", idAttr: firstIdAttr }],
                        primary_key: firstIdAttr,
                        description: "",
                        color: colors[Math.floor(Math.random() * colors.length)],
                    },
                },
            ],
        });
    }

    return (
        <>
            <input type="checkbox" id="toggle_step2_sidebar" />
            <div className="step2_sidebar">
                <div style={{ margin: "35px 0px 27px 21px", position: "relative" }}>
                    <Button variant="contained" style={{ backgroundColor: "#50C385 ", color: "white", textTransform: "capitalize" }} onClick={addEntity}>
                        <Plus /> Add Entity{" "}
                    </Button>
                    <label className="btn_toggle_sidebar_step2" htmlFor="toggle_step2_sidebar">
                        <ChevronLeft />
                    </label>
                </div>
                <div>
                    {step2Entities?.map((entity, index) => {
                        return <AccordionEntity key={entity.id} entity={entity} />;
                    })}
                </div>
            </div>
        </>
    );
}
