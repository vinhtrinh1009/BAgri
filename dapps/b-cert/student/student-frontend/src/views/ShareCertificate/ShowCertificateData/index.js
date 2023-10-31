import { makeStyles } from "@material-ui/core";
import BarForShareButton from "./BarForShareButton";
import DecryptedCertInfo from "./DecryptedCertInfo";
import { useSelector, useDispatch } from "react-redux";
import React, { useEffect, useState } from "react";
import { setEduProgram, setCertificateData } from "../redux";
import { getUser } from "src/utils/mng_user";
import { useSnackbar } from "notistack";
import { ERR_TOP_CENTER, SUCCESS_BOTTOM_CENTER } from "src/utils/snackbar-utils";

import axios from "axios";

const useStyels = makeStyles((theme) => ({
    root: {
        "& > *": {
            margin: theme.spacing(2, 0),
        },
    },
}));

export default function ShowCertificateData(props) {
    const cls = useStyels();
    const user = getUser();
    const dp = useDispatch();
    const { enqueueSnackbar } = useSnackbar();
    const loading = useSelector((state) => state.shareCertificateSlice.loading);

    useEffect(() => {
        fetchCertificateData();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    async function fetchCertificateData() {
        try {
            const response = await axios.get("/certificates/?user=" + user);
            dp(setCertificateData(response.data));
        } catch (error) {
            console.log(error.data);
            enqueueSnackbar(JSON.stringify(error.response.data.data), ERR_TOP_CENTER);
        }
    }
    return (
        <div>
            {!loading && <BarForShareButton></BarForShareButton>}
            <DecryptedCertInfo></DecryptedCertInfo>
        </div>
    );
}
