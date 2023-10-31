import { Box, makeStyles, Typography } from "@material-ui/core";
import { useSelector, useDispatch } from "react-redux";
import React, { useEffect, useState } from "react";

import { useSnackbar } from "notistack";

import View from "../../shared/View";
import EduProgramInfo from "./EduProgramInfo";
import ShowCertificateData from "./ShowCertificateData";
import { getUser } from "src/utils/mng_user";
import { ERR_TOP_CENTER, SUCCESS_BOTTOM_CENTER } from "src/utils/snackbar-utils";
import axios from "axios";
import { setEduProgram, setCertificateData } from "./redux";
import PDF from "./PDF_file/PDF";
// import ShowEncryptedInfo from "./ShowEncryptedInfo";
// import ShowDecryptInfo from "./ShowDecryptedEduInfo";

const useStyels = makeStyles((theme) => ({
    root: {
        "& > *": {
            margin: theme.spacing(2, 0),
        },
    },
}));

export default function ShareCertificate(props) {
    const cls = useStyels();
    const eduProgram = useSelector((state) => state.shareCertificateSlice.eduProgram);
    //   const show = useSelector((state) => state.shareCertificateSlice.show);
    const user = getUser();
    const dp = useDispatch();
    const { enqueueSnackbar } = useSnackbar();

    useEffect(() => {
        fetchEduProgram();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    async function fetchEduProgram() {
        try {
            const response = await axios.get("/student/" + user + "/");
            dp(setEduProgram(response.data));
        } catch (error) {
            enqueueSnackbar(JSON.stringify(error.response.data), ERR_TOP_CENTER);
        }
    }

    return (
        <View title="Chia sẻ bằng cấp">
            <Box className={cls.root}>
                <Box p={2} bgcolor="white">
                    <EduProgramInfo></EduProgramInfo>
                </Box>

                <ShowCertificateData></ShowCertificateData>

                {/* <Box p={2} bgcolor="white">
                    <PDF />
                </Box> */}
            </Box>
        </View>
    );
}
