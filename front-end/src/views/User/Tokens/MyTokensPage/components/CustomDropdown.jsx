import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import IconButton from "@mui/material/IconButton";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import MoreVertIcon from "@mui/icons-material/MoreVert";

const ITEM_HEIGHT = 48;

export const CustomDropdown = (token, token_type) => {
    const navigate = useNavigate();

    const [anchorEl, setAnchorEl] = useState(null);

    const open = Boolean(anchorEl);

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };
    function goViewDoc() {
        window.open(token?.token.user_defined_network ? "https://docs.v-chain.vn/apps/fabric-token/" : "https://docs.v-chain.vn/apps/ether-token/");
    }

    return (
        <div>
            <IconButton aria-label="more" id="long-button" aria-controls={open ? "long-menu" : undefined} aria-expanded={open ? "true" : undefined} aria-haspopup="true" onClick={handleClick}>
                <MoreVertIcon />
            </IconButton>

            <Menu
                id="long-menu"
                MenuListProps={{
                    "aria-labelledby": "long-button",
                }}
                anchorEl={anchorEl}
                open={open}
                onClose={handleClose}
                PaperProps={{
                    style: {
                        maxHeight: ITEM_HEIGHT * 4.5,
                        width: "max-content",
                    },
                }}
                anchorOrigin={{
                    vertical: "top",
                    horizontal: "right",
                }}
                transformOrigin={{
                    vertical: "top",
                    horizontal: "right",
                }}
            >
                <MenuItem key="detail" onClick={() => navigate(`/tokens/${token.token.id}/${token.token_type}`)}>
                    Detail
                </MenuItem>
                <MenuItem onClick={goViewDoc}>View Document</MenuItem>

                {/* <MenuItem key='transfer' onClick={() => navigate(`/tokens/transfer`)}>
                    Transfer
                </MenuItem>

                <MenuItem key='inspect' onClick={() => navigate(`/tokens/inspect`)}>
                    Inspect
                </MenuItem> */}
            </Menu>
        </div>
    );
};
