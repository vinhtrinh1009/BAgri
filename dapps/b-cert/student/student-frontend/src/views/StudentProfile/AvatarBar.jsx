import { Avatar, Box, Paper, Typography } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import { useSnackbar } from "notistack";
import { useDispatch, useSelector } from "react-redux";
import { getToken } from "src/utils/mng-token";
import { updateImgSrc } from "./redux";

const useStyles = makeStyles((theme) => ({
  root: {},
  avatar: {
    height: "128px",
    width: "128px",
    margin: "auto",
    position: "relative",
    cursor: "pointer",
    boxShadow: "0px 2px 8px -1px"
  },
  paper: {
    marginTop: "-64px",
    width: "100%",
  },
  name: {
    fontWeight: 600,
  },
  description: {
    fontWeight: 300,
    lineHeight: "1.5rem",
  },
}));

export default function AvatarBar() {
  const cls = useStyles();
  const studentName = useSelector((state) => state.studentProfileSlice.user.full_name);
  const user_id = useSelector((state) => state.studentProfileSlice.user.id);
  const avatarSrc = useSelector((state) => state.studentProfileSlice.user.avatar);
  const description = useSelector((state) => state.studentProfileSlice.description);
  const { enqueueSnackbar } = useSnackbar();
  const dp = useDispatch();

  async function hdChangeAvatar(e) {
    console.log(e.target.files[0]);

    const formData = new FormData();
    formData.append("avatar", e.target.files[0]);
    console.log(formData.getAll("user"));

    const res = await fetch(`${process.env.REACT_APP_BACKEND_URL}` + "/api/v1/update/avatar/" + user_id + "/", {
      method: "PATCH",
      headers: { Authorization: getToken() },
      body: formData,
    });

    if (!res.ok) {
      const err = await res.json();
      enqueueSnackbar("Something went wrong: " + JSON.stringify(err), {
        variant: "error",
        anchorOrigin: { vertical: "top", horizontal: "center" },
      });
    } else {
      const imgSrc = await res.json();
      console.log(res);
      // dp(updateImgSrc(imgSrc));
      enqueueSnackbar("Cập nhật Avatar thành công!", { variant: "success", anchorOrigin: { vertical: "bottom", horizontal: "right" } });
    }
  }

  return (
    <Box className={cls.root}>
      <label htmlFor="avatar">
        <input type="file" accept="image/*" id="avatar" style={{ display: "none" }} onChange={hdChangeAvatar} />
        <Avatar src={`${process.env.REACT_APP_BACKEND_URL}` + avatarSrc} className={cls.avatar}></Avatar>
      </label>
      <Paper className={cls.paper}>
        <Box textAlign="center" px={3} pb={3} pt={"96px"}>
          <Typography variant="h5" gutterBottom>
            Sinh viên Đại học
          </Typography>
          <Typography variant="h3" gutterBottom className={cls.name}>
            {studentName || "Nguyen Van A"}
          </Typography>
          <Typography variant="body2" className={cls.description}>
            {description ||
              "Quisque laoreet, sem a cursus blandit, lectus libero vestibulum purus, id malesuada risus sem id nulla. Curabitur suscipit, dolor at imperdiet dapibus, arcu massa semper enim, vitae consectetur nulla leo blandit nisi. Duis aliquam non turpis sit amet pellentesque. Sed arcu neque, sollicitudin vel ultricies"}
          </Typography>
        </Box>
      </Paper>
    </Box>
  );
}
