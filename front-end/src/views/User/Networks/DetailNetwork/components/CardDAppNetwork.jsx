import React from "react";
import { Media } from "reactstrap";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router";
import { NAVIGATE } from "src/redux/User/Networks/actionTypes";
import "../../index.scss";
import { imagePath } from "../../../../../constant/imagePath";

export default function CardDAppNetwork(props) {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const navigate_network = useSelector((state) => state.Network.navigate);

    let status = "";
    if (props.data.status === "CREATED") {
        status = "green";
    } else if (props.data.status === "CREATE_PENDING" || props.data.status === "DELETE_PENDING") {
        status = "yellow";
    } else {
        status = "red";
    }

    function getStatusColor() {
        if (props.data.status === "CREATED") {
            return "dot-notification-green";
        } else if (props.data.status === "CREATE_PENDING" || props.data.status === "DELETE_PENDING") {
            return "dot-notification-yellow";
        } else {
            return "dot-notification-red";
        }
    }

    const handleClick = () => {
        navigate(`/dapps/${props.data.dapp_id}`);
        dispatch({ type: NAVIGATE, payload: !navigate_network });
    };

    return (
        <div className="flex_box_col">
            <div className="cardDappInNetwork" onClick={() => handleClick()}>
                <div className="avatar">
                    <Media body className="img_custom" src={props.data.dapp_logo || imagePath.fabric} alt="#" />
                </div>
                <div className="dapp_name">{props.data.dapp_name}</div>
                <div className={`border_bottom ${getStatusColor()}`}></div>
            </div>
        </div>
    );
}
