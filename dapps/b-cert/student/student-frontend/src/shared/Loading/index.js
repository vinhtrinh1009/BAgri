import { makeStyles } from "@material-ui/core";
import { Skeleton } from "@material-ui/lab";

const useStyles = makeStyles((theme) => ({
  root: {
    height: "100vh",
    // padding: "10px",
    display: "grid",
    gridTemplateColumns: "1fr",
    gridTemplateRows: "64px auto",
    rowGap: "5px",
    "& *": {
      height: "100%",
    },
  },
  main: {
    display: "grid",
    gridTemplateColumns: "256px auto",
    columnGap: "5px",
  },
  sidebar: {
    display: "grid",
    gridTemplateColumns: "1fr",
    gridTemplateRows: "128px auto",
    rowGap: "5px",
  },
}));
export default function Loading(props) {
  const cls = useStyles();

  return (
    <div className={cls.root}>
      <div className={cls.topbar}>
        <Skeleton variant="rect"></Skeleton>
      </div>
      <div className={cls.main}>
        <div className={cls.sidebar}>
          <div className={cls.info}>
            <Skeleton variant="rect"></Skeleton>
          </div>
          <div className={cls.navlink}>
            <Skeleton variant="rect"></Skeleton>
          </div>
        </div>
        <div className={cls.content}>
          <Skeleton variant="rect"></Skeleton>
        </div>
      </div>
    </div>
  );
}
