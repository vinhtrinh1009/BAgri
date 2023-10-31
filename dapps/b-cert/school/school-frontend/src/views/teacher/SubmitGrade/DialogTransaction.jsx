import React, { useEffect, useState } from "react";
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Grid } from "@material-ui/core";
import axios from "axios";
import { useSnackbar } from "notistack";
import { ERR_TOP_CENTER } from "../../../utils/snackbar-utils";

export default function DialogTransaction(props) {
    const { open = false, handle_close = () => {}, tx_id = "" } = props;
    const { enqueueSnackbar } = useSnackbar();
    const [blockData, setBlockData] = useState({});
    const handleClose = () => {
        handle_close();
    };
    useEffect(() => {
        if (open == true) {
            (async () => {
                try {
                    const response = await axios.get("view-detail-tx/?txid=" + tx_id);
                    console.log(response.data);
                    setBlockData(response.data);
                } catch (error) {
                    console.error(error);
                    enqueueSnackbar("Load detail transaction fail!", ERR_TOP_CENTER);
                }
            })();
        }
    }, [open]);

    return (
        <Dialog open={open} onClose={handleClose} fullWidth maxWidth="md">
            <DialogTitle>Transaction Detail</DialogTitle>
            <DialogContent>
                <Grid container spacing={2}>
                    <Grid item xs={4}>
                        <div>Created at: </div>
                    </Grid>
                    <Grid item xs={8}>
                        <div>{new Date(Number(blockData?.tx_data?.payload_decode?.timestamp) * 1000).toLocaleString("it-IT")}</div>
                    </Grid>
                </Grid>
                <Grid container spacing={2}>
                    <Grid item xs={4}>
                        <div>By: </div>
                    </Grid>
                    <Grid item xs={8}>
                        <div>
                            {blockData.signer?.name || "Unknow"} - {blockData.signer?.signer_id || "Unknow"}
                        </div>
                    </Grid>
                </Grid>
                <Grid container spacing={2}>
                    <Grid item xs={4}>
                        <div>Action: </div>
                    </Grid>
                    <Grid item xs={8}>
                        <div>{blockData.tx_data?.payload_decode?.action || "Create"}</div>
                    </Grid>
                </Grid>
                <Grid container spacing={2}>
                    <Grid item xs={4}>
                        <div>Transaction id: </div>
                    </Grid>
                    <Grid item xs={8}>
                        <a
                            href={`${process.env.REACT_APP_EXPLORER_URL}/transactions/${tx_id}`}
                            target="_blank"
                            style={{ display: "block", width: "100%", overflow: "hidden", textOverflow: "ellipsis" }}
                        >
                            {tx_id}
                        </a>
                    </Grid>
                </Grid>
            </DialogContent>
            <DialogActions>
                <Button onClick={handleClose}>Close</Button>
            </DialogActions>
        </Dialog>
    );
}
