import React, { useLayoutEffect } from "react";
import { Breadcrumbs, Typography } from "@mui/material";
import { NavigateNext } from "@material-ui/icons";
import { Link } from "react-router-dom";
import { useSelector } from "react-redux";

export default function BreadcrumbCt(props) {
    const { path = [] } = props;
    const folderOwner = useSelector((stores) => stores.Storage.data?.owner);
    const currentUser = useSelector((stores) => stores.User?.user);

    return (
        <div style={{ width: "calc(100% - 160px)" }}>
            <Breadcrumbs maxItems={3} itemsAfterCollapse={2} separator={<NavigateNext fontSize="small" />} aria-label="breadcrumb">
                {path.map((item, index) => {
                    if (index == 0) {
                        if (folderOwner?.username != currentUser?.username) {
                            return (
                                <Link underline="hover" key={item.folder_id + index} color="inherit" to={`/storages/platform-artifact`}>
                                    <span style={{ color: "#2897E8" }}>{item.name}</span>
                                </Link>
                            );
                        }
                        return (
                            <Link underline="hover" key={item.folder_id + index} color="inherit" to={`/storages/`}>
                                <span style={{ color: "#2897E8" }}>{item.name}</span>
                            </Link>
                        );
                    } else {
                        return (
                            <Link underline="hover" key={item.folder_id + index} color="inherit" to={`/storages/${item.folder_id}`}>
                                <span style={{ color: "#2897E8" }}>{item.name}</span>
                            </Link>
                        );
                    }
                })}
            </Breadcrumbs>
        </div>
    );
}
