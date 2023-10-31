import React, { useEffect, useState } from "react";
import { isPositiveNumber, isStringNumber } from "src/utils/stringhandle";
import TextField from "@mui/material/TextField";

export default function InputNumber(props) {
    const { className = "", defaultValue, label, variant, OnChange, value, onlyPositive = false, required = false, style = {} } = props;
    const [helperText, setHelperText] = useState("");

    function checkIsPositive(str) {
        if (str === "" && required === true) {
            setHelperText("*Required!");
        } else if (onlyPositive == true) {
            if (isPositiveNumber(str)) setHelperText("");
            else setHelperText("*Please! Enter a positive integer!!!");
        } else if (onlyPositive == false) {
            if (isStringNumber(str)) setHelperText("");
            else setHelperText("*Please! Enter a number!!!");
        }
    }
    function checkInput(event) {
        checkIsPositive(event.target.value);
        OnChange(event);
    }

    useEffect(() => {
        if (onlyPositive && defaultValue) checkIsPositive(defaultValue);
        if (onlyPositive && value) checkIsPositive(value);
    }, []);

    return (
        <div className={className} style={{ ...style, position: "relative" }}>
            <TextField inputMode="numeric" label={label} variant={variant} fullWidth onChange={checkInput} required={required} value={value} size="small" defaultValue={defaultValue} />
            <div style={{ marginBottom: "31px", fontSize: "small", color: "red", position: "absolute" }}>{helperText}</div>
        </div>
    );
}
