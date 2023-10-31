import { Box, Button, Grid, IconButton, InputAdornment, makeStyles, Paper, TextField, Typography } from "@material-ui/core";
import AccountBalanceWalletIcon from "@material-ui/icons/AccountBalanceWallet";
import axios from "axios";
import "date-fns";
import { useSnackbar } from "notistack";
import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { requirePrivateKeyHex } from "../../../utils/keyholder";
import { ERR_TOP_CENTER, INFO_TOP_CENTER, SUCCESS_BOTTOM_CENTER, SUCCESS_TOP_CENTER } from "../../../utils/snackbar-utils";
import { setProfile, setReload } from "./redux";
import { getUser, setUniversity } from "src/utils/mng_user";
const { PrivateKey } = require("eciesjs");

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
}));

export default function ProfileForm() {
    const cls = useStyles();
    const profile = useSelector((state) => state.profileSlice);
    const [state, setState] = useState(profile);
    const dp = useDispatch();
    const { enqueueSnackbar } = useSnackbar();
    const user = getUser();
    const disable = profile.state;

    async function hdSubmitRegister(e) {
        // if (!profile.avatar) {
        //   return enqueueSnackbar("Cần bổ sung ảnh đại diện trước khi đăng kí tham gia", INFO_TOP_CENTER);
        // }
        if (!state.university_id) return enqueueSnackbar("University ID missing", INFO_TOP_CENTER);

        try {
            //   const privateKeyHex = await requirePrivateKeyHex(enqueueSnackbar);
            enqueueSnackbar("Wait for sending request! ", SUCCESS_TOP_CENTER);
            let response = await axios.post("/register-university/", {
                university_id: state.university_id,
                name: state.university_name,
                email: state.email,
                address: state.address,
                phone: state.phone,
                user: user,
                avatar: profile.avatar,
                description: state.description,
            });
            enqueueSnackbar("Đăng kí tham gia thành công", SUCCESS_TOP_CENTER);
            // dp(setProfile({ ...state, avatar: profile.avatar, state: true }));
            dp(setReload());
            setUniversity(response.data.id);
        } catch (error) {
            console.error(error);
            console.log(typeof error.response.data);
            if (error.response) enqueueSnackbar(JSON.stringify(error.response.data), ERR_TOP_CENTER);
        }
    }

    async function hdSubmitUpdate(e) {
        // if (!profile.avatar) {
        //   return enqueueSnackbar("Cần bổ sung ảnh đại diện trước khi đăng kí tham gia", INFO_TOP_CENTER);
        // }

        try {
            //   const privateKeyHex = await requirePrivateKeyHex(enqueueSnackbar);
            await axios.patch("/update-university-info/" + profile.id + "/", {
                user: user,
                profile: {
                    name: state.university_name,
                    email: state.email,
                    address: state.address,
                    phone: state.phone,
                    avatar: profile.avatar,
                    description: state.description,
                },
            });
            enqueueSnackbar("Cập nhật thông tin thành công", SUCCESS_TOP_CENTER);
            dp(setProfile({ ...state, avatar: profile.avatar, state: "true" }));
        } catch (error) {
            console.error(error);
            console.log(typeof error.response.data);
            if (error.response) enqueueSnackbar(JSON.stringify(error.response.data), ERR_TOP_CENTER);
        }
    }

    // get public key to fill the form
    async function hdSelectAccountFromWallet() {
        const privateKeyHex = await requirePrivateKeyHex(enqueueSnackbar);
        setState({ ...state, publicKey: PrivateKey.fromHex(privateKeyHex).publicKey.toHex(true) });
    }

    return (
        <Box className={cls.root}>
            <Paper className={cls.head}>
                <Typography variant="h3">Thông tin Trường học</Typography>
                <Typography variant="subtitle1">Thông tin này sẽ được hiển thị với BGD và các Trường khác</Typography>
            </Paper>
            <Box className={cls.body}>
                <Paper>
                    <Box className={cls.box}>
                        <TextField
                            InputLabelProps={{ shrink: true }}
                            fullWidth
                            label="Tên Trường"
                            value={state?.university_name}
                            onChange={(e) => setState({ ...state, university_name: e.target.value })}
                            // disabled={disable}
                        ></TextField>
                        <TextField
                            InputLabelProps={{ shrink: true }}
                            fullWidth
                            label="Mã Trường (theo công bố của Bộ Giáo dục)"
                            value={state?.university_id}
                            onChange={(e) => setState({ ...state, university_id: e.target.value })}
                            disabled={profile.id != ""}
                        ></TextField>
                        <TextField
                            InputLabelProps={{ shrink: true }}
                            fullWidth
                            label="Địa chỉ"
                            value={state?.address}
                            onChange={(e) => setState({ ...state, address: e.target.value })}
                            //   disabled={disable}
                        ></TextField>
                        <Grid container spacing={2}>
                            <Grid item xs={12} md={6}>
                                <TextField
                                    InputLabelProps={{ shrink: true }}
                                    fullWidth
                                    label="Email"
                                    value={state?.email}
                                    onChange={(e) => setState({ ...state, email: e.target.value })}
                                    //   disabled={disable}
                                ></TextField>
                            </Grid>
                            <Grid item xs={12} md={6}>
                                <TextField
                                    InputLabelProps={{ shrink: true }}
                                    fullWidth
                                    label="Số điện thoại"
                                    value={state?.phone}
                                    onChange={(e) => setState({ ...state, phone: e.target.value })}
                                    //   disabled={disable}
                                ></TextField>
                            </Grid>
                        </Grid>
                        <TextField
                            InputLabelProps={{ shrink: true }}
                            fullWidth
                            label="Mô tả khác"
                            multiline
                            rows={4}
                            value={state?.description}
                            onChange={(e) => setState({ ...state, description: e.target.value })}
                            //   disabled={disable}
                        ></TextField>
                        {!profile.id ? (
                            <Box textAlign="right">
                                <Button color="primary" variant="contained" onClick={hdSubmitRegister}>
                                    Đăng kí tham gia
                                </Button>
                            </Box>
                        ) : (
                            <Box textAlign="right">
                                <Button color="primary" variant="contained" onClick={hdSubmitUpdate}>
                                    Sửa thông tin trường
                                </Button>
                            </Box>
                        )}
                    </Box>
                </Paper>
            </Box>
        </Box>
    );
}
