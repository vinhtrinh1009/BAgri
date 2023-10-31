import { makeStyles, TextField } from "@material-ui/core";
import axios from "axios";
import { useSnackbar } from "notistack";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router";
import { ERR_TOP_CENTER } from "../../utils/snackbar-utils";
import { setDecodedData, setDecodedTokenAndEduProgramOnBKC } from "../redux";
import React, { useEffect, useState } from "react";
import Page from "../../shared/Page";

const useStyles = makeStyles((theme) => ({
    root: {
        height: "100%",
        overflow: "hidden",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        backgroundImage: "url('static/images/blockchain.jpg')",
        backgroundSize: "cover",
        backgroundPosition: "center",
    },
    box: {
        flexBasis: "70%",
        display: "flex",
    },
    inputToken: {
        background: "rgba(0,0,0,0.85)",
        borderRadius: "5px",
        // boxShadow: '0 0 0 7px rgb(255 255 255 / 30%)',
        "& .MuiInputBase-input": {
            color: "white",
        },
    },
}));

export default function Verify(props) {
    const cls = useStyles();
    const [data, setData] = useState("");
    async function enterKeyPress(e) {
        if (e.key === "Enter") {
            checkTocken(data);
        }
    }

    async function hdPasteToken(e) {
        const token = e.clipboardData.getData("Text");
        checkTocken(token);
    }

    async function checkTocken(token) {
        window.location.href = "/ket-qua/" + token;
    }

    return (
        <Page title="Xac thuc bang cap" className={cls.root}>
            <div className={cls.box}>
                <TextField
                    className={cls.inputToken}
                    onChange={(e) => {
                        setData(e.target.value);
                    }}
                    variant="outlined"
                    label="Token"
                    fullWidth
                    autoFocus
                    // onPaste={hdPasteToken}
                    onKeyPress={enterKeyPress}
                ></TextField>
            </div>
        </Page>
    );
}
