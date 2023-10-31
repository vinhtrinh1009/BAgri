import { Box, Button, Grid, IconButton, Paper } from "@material-ui/core";
import { Pagination } from "@material-ui/lab";
import axios from "axios";
import React, { useEffect, useState } from "react";
import { Eye, EyeOff } from "react-feather";
import Page from "../../../shared/Page";
import DialogTransaction from "../../teacher/SubmitGrade/DialogTransaction";

const TransactionType = {
    1: "Create",
    2: "Update",
    0: "None",
};

export default function Transactions() {
    const [listTransaction, setListTransaction] = useState({ data: [], total: 0 });
    const [txModel, setTxModel] = useState({ open: false, tx_id: "" });
    const [curPage, setCurPage] = useState(1);
    const handleChangePage = (event, value) => {
        getDataPage(value);
        setCurPage(value);
    };
    async function getDataPage(page_num) {
        try {
            const res = await axios.get("/get_all_transaction/?page=" + page_num);
            console.log(res.data);

            setListTransaction({ data: res.data.data, total: res.data.total });
        } catch (error) {
            console.log(error);
        }
    }
    useEffect(() => {
        getDataPage(1);
    }, []);

    return (
        <Page title="Thông tin giao dịch">
            <Paper style={{ padding: "20px" }}>
                <Grid container spacing={2} style={{ fontWeight: "bold", fontSize: "larger", marginBottom: "20px" }}>
                    <Grid item xs={1}>
                        STT
                    </Grid>
                    <Grid item xs={3}>
                        Transaction id
                    </Grid>
                    <Grid item xs={2}>
                        Created at
                    </Grid>
                    <Grid item xs={3}>
                        Created By
                    </Grid>
                    <Grid item xs={2}>
                        Type
                    </Grid>
                    <Grid item xs={1}>
                        Detail
                    </Grid>
                </Grid>
                {listTransaction.data.map((item, index) => {
                    return (
                        <Grid container spacing={3} key={"tran" + item.tx_data.data.header_signature}>
                            <Grid item xs={1}>
                                {index + 1}
                            </Grid>
                            <Grid item xs={3}>
                                <div style={{ width: "100%", overflow: "hidden", textOverflow: "ellipsis" }}>{item.tx_data.data.header_signature}</div>
                            </Grid>
                            <Grid item xs={2}>
                                {new Date(Number(item.tx_data.payload_decode.timestamp) * 1000).toLocaleString("it-IT")}
                            </Grid>
                            <Grid item xs={3}>
                                {item.signer.name}
                            </Grid>
                            <Grid item xs={2}>
                                {item.tx_data.payload_decode.action || "CREATE"}
                            </Grid>
                            <Grid item xs={1} style={{ cursor: "pointer" }}>
                                <a href={`${process.env.REACT_APP_EXPLORER_URL}/transactions/${item.tx_data.data.header_signature}`} target="_blank">
                                    <IconButton>
                                        <Eye></Eye>
                                    </IconButton>
                                </a>
                            </Grid>
                        </Grid>
                    );
                })}
                <Pagination count={Math.ceil(listTransaction.total / 10)} page={curPage} onChange={handleChangePage} />
            </Paper>
            <DialogTransaction
                open={txModel.open}
                handle_close={() =>
                    setTxModel((prev) => {
                        return { ...prev, open: false };
                    })
                }
                tx_id={txModel.tx_id}
            />
        </Page>
    );
}
