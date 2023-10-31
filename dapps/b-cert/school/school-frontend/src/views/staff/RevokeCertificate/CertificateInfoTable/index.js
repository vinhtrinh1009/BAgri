import { Divider, Paper } from "@material-ui/core";
import React from "react";
import Body from "./Body";
import Title from "./Title";

export default function CertificateInfoTable({ cert }) {
  return (
    <Paper>
      <Title cert={cert}></Title>
      <Divider></Divider>
      <Body cert={cert}></Body>
    </Paper>
  );
}
