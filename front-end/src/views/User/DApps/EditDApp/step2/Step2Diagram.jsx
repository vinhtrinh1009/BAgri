import React, { useCallback, useState } from "react";
import { useSelector } from "react-redux";
import { useDispatch } from "react-redux";
import { SELECTED_NODE, STEP2_ENTITIES, STEP2_RELATIONSHIPS, STATE_CONNECTING_ENTITY } from "src/redux/User/DApps/actionTypes";
import ReactFlow, { removeElements, addEdge, MiniMap, Controls, Background, isNode, ReactFlowProvider } from "react-flow-renderer";

import { findNodeById, swapSourceTarget, reverseString } from "../../NewDApp/components/step2/utils";
import { relationShipType } from "../../../../../constant/relationShipType";
import CustomNodeFlow from "../../NewDApp/components/custom_react_flow/CustomNodeFlow";
import FloatingEdge from "../../NewDApp/components/custom_react_flow/FloatingEdge";
import FloatingConnectionLine from "../../NewDApp/components/custom_react_flow/FloatingConnectionLine";

export default function Step2Diagram() {
    const dispatch = useDispatch();
    const [zoom, setZoom] = useState(1);
    const step2Entities = useSelector((state) => state.DApp.step2Entities);
    const step2Relationships = useSelector((state) => state.DApp.step2Relationships);
    const layout = useSelector((state) => state.Storage.layout);
    const isConnecting = useSelector((state) => state.DApp.isConnectingEntity);

    const onElementClick = (event, element) => {
        if (!element.target) {
            document.querySelector(`label[for='${element.id}-header']`).click();
            // dispatch({ type: SELECTED_NODE, payload: element.id });
        }
    };
    const nodeTypes = {
        customNode: CustomNodeFlow,
    };

    const edgeTypes = {
        customEdge: FloatingEdge,
    };
    const onLoad = useCallback((instance) => {
        instance.fitView();
    }, []);
    const onNodeDragStop = (event, node) => {
        step2Entities.map((entity, key) => {
            if (entity.id === node.id) {
                entity.position = node.position;
            }
        });
        dispatch({ type: STEP2_ENTITIES, payload: step2Entities });
        const newStep2Relation = step2Relationships.map((relationship) => {
            if (relationship.id.includes(node.id)) {
                if (node.id === relationship.source) {
                    const otherNode = findNodeById(step2Entities, step2Entities.length, relationship.target);
                    if (node.position.x > otherNode.position.x) {

                        const revertTypeConnect = reverseString(relationship.data.type);
                        return {
                            source: relationship.target,
                            sourceHandle: relationship.target + "sright",
                            target: relationship.source,
                            targetHandle: relationship.source + "tleft",
                            id: relationship.target + "-" + revertTypeConnect + "-" + relationship.source,
                            data: {
                                id: relationship.target + "-" + revertTypeConnect + "-" + relationship.source,
                                source: relationship.target,
                                target: relationship.source,
                                type: revertTypeConnect,
                            },
                            type: "customEdge",
                        };
                    }
                } else {
                    const otherNode = findNodeById(step2Entities, step2Entities.length, relationship.source);
                    if (node.position.x < otherNode.position.x) {

                        const revertTypeConnect = reverseString(relationship.data.type);
                        return {
                            source: relationship.target,
                            sourceHandle: relationship.target + "sright",
                            target: relationship.source,
                            targetHandle: relationship.source + "tleft",
                            id: relationship.target + "-" + revertTypeConnect + "-" + relationship.source,
                            data: {
                                id: relationship.target + "-" + revertTypeConnect + "-" + relationship.source,
                                source: relationship.target,
                                target: relationship.source,
                                type: revertTypeConnect,
                            },
                            type: "customEdge",
                        };
                    }
                }
            }
            return relationship;
        });
        dispatch({ type: STEP2_RELATIONSHIPS, payload: newStep2Relation });
    };
    const checkAlreadyConnected = (id1, id2) => {
        const numberConnection = step2Relationships.length;
        for (let i = 0; i < numberConnection; i++) {
            if (step2Relationships[i].id.includes(id1) && step2Relationships[i].id.includes(id2)) {
                return true;
            }
        }
        return false;
    };
    const connectTwoNode = (params, idSource, idTarget) => {
        dispatch({
            type: STEP2_RELATIONSHIPS,
            payload: [
                ...step2Relationships,
                {
                    ...params,
                    id: idSource + "-" + relationShipType.OneToOne + "-" + idTarget,
                    data: {
                        ...params.data,
                        id: idSource + "-" + relationShipType.OneToOne + "-" + idTarget,
                        source: idSource,
                        target: idTarget,
                        type: relationShipType.OneToOne,
                    },
                    type: "customEdge",
                },
            ],
        });
    };
    const onConnect = (params) => {
        if (params.source !== params.target && checkAlreadyConnected(params.source, params.target) === false) {
            const lengthEntity = step2Entities.length;
            const node1 = findNodeById(step2Entities, lengthEntity, params.source);
            const node2 = findNodeById(step2Entities, lengthEntity, params.target);
            if (node1.position.x > node2.position.x) {
                connectTwoNode(swapSourceTarget(params), node2.id, node1.id);
            } else {
                connectTwoNode(params, node1.id, node2.id);
            }
        }
    };
    const onConnectStart = (event) => {
        dispatch({ type: STATE_CONNECTING_ENTITY, payload: true });
    };
    const onConnectEnd = (event) => {
        dispatch({ type: STATE_CONNECTING_ENTITY, payload: false });
    };
    return (
        <ReactFlowProvider>
            {/* <button onClick={() => setZoom((prev) => prev + 1)}>click</button> */}
            <div className={isConnecting ? "is_connecting reactflow-wrapper" : "reactflow-wrapper"}>
                <ReactFlow
                    minZoom={1}
                    maxZoom={1}
                    style={{ width: "100%", height: "calc(100vh - 322px)", zIndex: "0" }}
                    elements={[...step2Entities, ...step2Relationships]}
                    nodeTypes={nodeTypes}
                    edgeTypes={edgeTypes}
                    onElementClick={onElementClick}
                    onlyRenderVisibleElements={false}
                    onConnect={onConnect}
                    onConnectStart={onConnectStart}
                    onConnectEnd={onConnectEnd}
                    onLoad={onLoad}
                    snapToGrid={true}
                    snapGrid={[15, 15]}
                    key="step2Diagram"
                    onNodeDragStop={onNodeDragStop}
                    nodesDraggable={true}
                    connectionLineComponent={FloatingConnectionLine}
                    defaultZoom={1}
                >
                    <MiniMap
                        nodeColor={(node) => {
                            return node.data.color;
                        }}
                    />
                    <Controls />
                    <Background variant="dots" color="#f1f6f8" />
                </ReactFlow>
            </div>
        </ReactFlowProvider>
    );
}
