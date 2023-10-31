import React from "react";
import Grid from "@mui/material/Grid";
import "../index.scss";
import { styled } from "@mui/material/styles";
import Paper from "@mui/material/Paper";
import { Button } from "@material-ui/core";

export default function Plan() {
    return (
        <>
            <h1 className=" d-center" style={{ marginTop: "48px", marginBottom: "40px" }}>
                {"Upgrade Plan"}
            </h1>
            <Grid container md={12} xs={12} spacing={2} className="d-center">
                <Grid item md={3} xs={3}>
                    <Paper className="plan-paper current">
                        <div className="plan-header">free</div>
                        <div className="plan-price">$0 permonth</div>
                        <br />
                        <div className="plan-body">1 Network</div>
                        <div className="plan-body">1 DApp</div>
                        <div className="plan-body">50GB</div>
                    </Paper>
                </Grid>
                <Grid item md={3} xs={3}>
                    <Paper className="plan-paper">
                        <div className="plan-header">pro</div>
                        <div className="plan-price">$29,99 permonth</div>
                        <br />
                        <div className="plan-body">2 Network</div>
                        <div className="plan-body">2 DApp</div>
                        <div className="plan-body">10GB storage</div>
                        <div className="plan-body">Encrypt data</div>
                        <br />
                        <br />
                        <div className="plan-btn">
                            <Button variant="contained" color="primary">
                                Upgrade Plan
                            </Button>
                        </div>
                    </Paper>
                </Grid>
                <Grid item md={3} xs={3}>
                    <Paper className="plan-paper">
                        <div className="plan-header">enterprise</div>
                        <div className="plan-price">$49,99 permonth</div>
                        <br />
                        <div className="plan-body">5 Network</div>
                        <div className="plan-body">5 DApp</div>
                        <div className="plan-body">25GB storage</div>
                        <div className="plan-body">Encrypt data</div>
                        <br />
                        <br />
                        <div className="plan-btn">
                            <Button variant="contained" color="primary">
                                Upgrade Plan
                            </Button>
                        </div>
                    </Paper>
                </Grid>
            </Grid>
            <div style={{ height: "150px" }}></div>
        </>
    );
}
