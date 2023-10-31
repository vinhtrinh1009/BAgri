import { Box, makeStyles, Paper, Typography } from "@material-ui/core";
import DragnDropZone from "../../../shared/DragnDropZone";
import { useTheme } from "@material-ui/core/styles";

import axios from "axios";
import "date-fns";
import { useSnackbar } from "notistack";
import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { ERR_TOP_CENTER, INFO_TOP_CENTER, SUCCESS_BOTTOM_CENTER } from "../../../utils/snackbar-utils";
import { startUploadFile, uploadFileFail, uploadFileSuccess } from "./redux";
import { getUser, getUniversity } from "src/utils/mng_user";

const useStyles = makeStyles((theme) => ({
    root: {
        "& .MuiFormLabel-root.Mui-disabled": {
            color: theme.palette.primary.main,
        },
        "& .MuiInputBase-input.Mui-disabled": {
            color: "black",
        },
    },
    head: {
        width: "95%",
        margin: "auto",
        padding: theme.spacing(2.5, 2),
        backgroundColor: theme.palette.primary.main,
        color: "white",
        position: "relative", // this bring head foreground
    },
    body: { width: "100%", marginTop: "-32px" },
    box: {
        padding: theme.spacing(8, 3, 3, 3),
        "& > *": {
            marginBottom: theme.spacing(4),
            "&:last-child": {
                marginBottom: 0,
            },
        },
    },
    selectEmpty: {
        marginTop: theme.spacing(2),
    },
}));

export default function UploadClassForm() {
    const theme = useTheme();
    const cls = useStyles();
    const dp = useDispatch();
    const { enqueueSnackbar } = useSnackbar();
    const user = getUser();
    const university = getUniversity();
    const uploading = useSelector((state) => state.classSlice.uploading);

    async function hdUploadFile(files) {
        dp(startUploadFile());
        const formData = new FormData();
        formData.append("university", university);
        formData.append("excel-file", files[0]);
        try {
            const response = await axios.post("/create-class/", formData);
            enqueueSnackbar("Upload file thành công!", SUCCESS_BOTTOM_CENTER);
            dp(uploadFileSuccess(response.data));
        } catch (error) {
            console.error(error);
            if (error.response) enqueueSnackbar(JSON.stringify(error.response.data), ERR_TOP_CENTER);
            dp(uploadFileFail());
        }
    }
    return (
        <Box className={cls.root}>
            <Paper className={cls.head}>
                <Typography variant="h3">Thông tin tạo lớp</Typography>
            </Paper>
            <Box className={cls.body}>
                <Paper>
                    <DragnDropZone onDropAccepted={hdUploadFile} uploading={uploading}></DragnDropZone>
                </Paper>
            </Box>
        </Box>
    );
}
