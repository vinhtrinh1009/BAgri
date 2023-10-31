import DateFnsUtils from "@date-io/date-fns";
import { Box, Button, FormControl, Grid, InputLabel, makeStyles, MenuItem, Paper, Select, TextField, Typography } from "@material-ui/core";
import { KeyboardDatePicker, MuiPickersUtilsProvider } from "@material-ui/pickers";
import "date-fns";
import { useSnackbar } from "notistack";
import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getToken } from "src/utils/mng-token";
import { setProfile } from "./redux";
import axios from "axios";
import { ERR_TOP_CENTER, INFO_TOP_CENTER, SUCCESS_BOTTOM_CENTER } from "src/utils/snackbar-utils";

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
            marginBottom: theme.spacing(3),
            "&:last-child": {
                marginBottom: 0,
            },
        },
    },
}));

export default function ProfileForm() {
    const cls = useStyles();
    const studentProfile = useSelector((state) => state.studentProfileSlice);
    const user_id = localStorage.getItem("user");
    const [state, setState] = useState(studentProfile);
    const [lastUpdatedState, setCheckPointState] = useState(state);
    const { enqueueSnackbar } = useSnackbar();
    const dp = useDispatch();

    console.log(studentProfile);

    async function hdSubmit(e) {
        try {
            e.preventDefault();
            if (lastUpdatedState === state) {
                enqueueSnackbar("Nothing changed", { variant: "info", anchorOrigin: { vertical: "bottom", horizontal: "center" } });
                return;
            }

            try {
                //   const privateKeyHex = await requirePrivateKeyHex(enqueueSnackbar);
                await axios.post("student/" + user_id + "/", {});
                enqueueSnackbar("Đăng kí tham gia thành công", SUCCESS_BOTTOM_CENTER);
                // dp(setProfile({ ...state, avatar: profile.avatar, state: "true" }));
            } catch (error) {
                console.error(error);
                console.log(typeof error.response.data);
                if (error.response) enqueueSnackbar(JSON.stringify(error.response.data), ERR_TOP_CENTER);
            }
        } catch (error) {
            alert(error);
        }
    }

    return (
        <Box className={cls.root}>
            <Paper className={cls.head}>
                <Typography variant="h3">Thông tin cá nhân</Typography>
                <Typography variant="subtitle1">Chỉnh sửa lại thông tin cá nhân (nếu cần)</Typography>
            </Paper>
            <Box className={cls.body}>
                <Paper>
                    <Box className={cls.box}>
                        {/* row 1 */}
                        <Grid container spacing={2}>
                            <Grid item xs={6}>
                                <TextField
                                    InputLabelProps={{ shrink: true }}
                                    id="name"
                                    label="Họ và tên"
                                    fullWidth
                                    // margin="normal"
                                    value={state?.user.full_name}
                                    disabled={true}
                                    // onChange={(e) => setState({ ...state, [user.full_name]: e.target.value })}
                                ></TextField>
                            </Grid>
                            <Grid item xs={6}>
                                <MuiPickersUtilsProvider utils={DateFnsUtils}>
                                    <KeyboardDatePicker
                                        // margin="normal"
                                        id="birthday"
                                        label="Ngày sinh"
                                        views={["year", "month", "date"]}
                                        openTo="year"
                                        disableFuture
                                        autoOk
                                        format="dd/MM/yyyy"
                                        value={state?.birthDay}
                                        disabled={true}
                                        // onChange={(selectedDate) => setState({ ...state, birthDay: selectedDate })}
                                        KeyboardButtonProps={{
                                            "aria-label": "change date",
                                        }}
                                    />
                                </MuiPickersUtilsProvider>
                            </Grid>
                        </Grid>
                        <Grid container spacing={2}>
                            <Grid item xs={6}>
                                <TextField
                                    InputLabelProps={{ shrink: true }}
                                    fullWidth
                                    margin="normal"
                                    label="Email"
                                    value={state?.user.email}
                                    disabled={true}
                                    // onChange={(e) => setState({ ...state, email: e.target.value })}
                                ></TextField>
                            </Grid>
                            <Grid item xs={6}>
                                <TextField
                                    InputLabelProps={{ shrink: true }}
                                    fullWidth
                                    margin="normal"
                                    label="Số điện thoại"
                                    value={state?.user.phone}
                                    disabled={true}
                                    // onChange={(e) => setState({ ...state, phone: e.target.value })}
                                ></TextField>
                            </Grid>
                        </Grid>
                        {/* row 3 */}
                        <Grid container spacing={2}>
                            <Grid item xs={12}>
                                <TextField
                                    InputLabelProps={{ shrink: true }}
                                    fullWidth
                                    margin="normal"
                                    xs={12}
                                    label="Nơi ở hiện tại"
                                    value={state?.user.address}
                                    disabled={true}
                                    // onChange={(e) => setState({ ...state, address: e.target.value })}
                                ></TextField>
                            </Grid>
                        </Grid>

                        {/* row 4 */}
                        <Grid container spacing={2}>
                            <Grid item xs={12}>
                                <TextField
                                    InputLabelProps={{ shrink: true }}
                                    fullWidth
                                    margin="normal"
                                    xs={12}
                                    label="Public Key"
                                    multiline
                                    rows={4}
                                    value={state?.user.public_key}
                                    disabled={true}
                                    // onChange={(e) => setState({ ...state, description: e.target.value })}
                                ></TextField>
                            </Grid>
                        </Grid>
                    </Box>
                </Paper>
            </Box>
        </Box>
    );
}
