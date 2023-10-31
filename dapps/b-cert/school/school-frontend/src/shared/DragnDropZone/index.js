import { Paper } from "@material-ui/core";
import { useSnackbar } from "notistack";
import React, { useMemo } from "react";
import { useDropzone } from "react-dropzone";
import MdInfinite from "react-ionicons/lib/MdInfinite";
import UseAnimations from "react-useanimations";
import arrowDown from "react-useanimations/lib/arrowDown";
import { ERR_TOP_CENTER } from "../../utils/snackbar-utils";

const baseStyle = {
  flex: 1,
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  padding: "40px",
  borderWidth: 4,
  borderRadius: 4,
  borderColor: "#eeeeee",
  borderStyle: "dashed",
  cursor: 'pointer',
  // backgroundColor: "#fafafa",
  // backgroundColor: "white",
  // color: "#bdbdbd",
  color: "rgba(0,0,0,0.7)",
  // outline: "1px solid #eeeeee",
  transition: "border .24s ease-in-out",
};

const activeStyle = {
  borderColor: "#2196f3",
};

const acceptStyle = {
  borderColor: "#00e676",
};

const rejectStyle = {
  borderColor: "#ff1744",
};

export default function DragnDropZone({ onDropAccepted, uploading }) {
  const { enqueueSnackbar } = useSnackbar();

  function onDropRejected(fileRejections) {
    enqueueSnackbar("Chỉ chấp nhận excel file!", ERR_TOP_CENTER);
  }

  const { getRootProps, getInputProps, isDragActive, isDragAccept, isDragReject } = useDropzone({
    accept: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    onDropRejected,
    onDropAccepted,
  });

  const style = useMemo(
    () => ({
      ...baseStyle,
      ...(isDragActive ? activeStyle : {}),
      ...(isDragAccept ? acceptStyle : {}),
      ...(isDragReject ? rejectStyle : {}),
      
    }),
    [isDragActive, isDragReject, isDragAccept]
  );

  return (
    <Paper>
      <div {...getRootProps({ style })}>
        <input {...getInputProps()} />
        {uploading ? (
          <>
            <MdInfinite rotate={true} fontSize="75px" />
            <p>Uploading...</p>
          </>
        ) : (
          <>
            <UseAnimations animation={arrowDown} size={75} />
            <p>Kéo thả file excel vào đây. Hoặc click để tải file lên.</p>
          </>
        )}
      </div>
    </Paper>
  );
}
