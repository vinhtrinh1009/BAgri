import React, { useEffect, useState } from "react";
import { PlusSquare } from "react-feather";
import { useDispatch, useSelector } from "react-redux";
import avatar_placeholder from "../../../../../assets/images/user/7.jpg";
import more from "../../../../../assets/images/user/three-horizontal-dots-icon-6.png";
import { Row, Col, Card, CardHeader, CardFooter, CardBody, Media, Dropdown, DropdownToggle, DropdownMenu } from "reactstrap";
import { Table, TableContainer, TableHead, TableRow, TableCell, TableBody, Paper, Pagination } from "@mui/material";
import { Link } from "react-router-dom";
import { DISPLAY_TOKEN } from "../../../../../redux/User/Tokens/actionTypes";
import { tokensActions } from "src/redux/User/Tokens/reducer";
import PropTypes from "prop-types";
import { getFTTokens, getNFTTokens } from "src/services/User/tokens";
import CustomTablePagination from "./CustomTablePagination";
import { CustomDropdown } from "./CustomDropdown";
import { imagePath } from "../../../../../constant/imagePath";
import { OPEN_ERROR_ALERT } from "../../../../../redux/User/Alerts/actionTypes";
// import { getFabricTokens } from 'src/services/User/tokens';

const CardToken = (prop) => {
    const dispatch = useDispatch();

    const pageSize = 10;

    const [ftPageCount, setFTPageCount] = useState(1);
    const [ftCurrentPage, setFTCurrentPage] = useState(1);
    const [ftPageData, setFTPageData] = useState([{}]);

    useEffect(async () => {
        try {
            let response = await getFTTokens({ page: ftCurrentPage });
            setFTPageData(response.data.results);
            setFTPageCount(Math.ceil(response.data.count / pageSize));
        } catch (error) {
            dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Something wrong happened! Or no more data!" } });
        }
    }, []);

    // useEffect(async () => {
    //     getFabricTokens()
    //     .then(res => setFabricFtData(res.data))
    //     .catch(err => alert("Something wrong happened. Please reload the page."))
    // }, [])

    // console.log(ftPageData)

    async function handleChangePage(event, value) {
        console.log(value);
        try {
            let response = await getFTTokens({ page: value });
            setFTPageData(response.data.results);
            setFTPageCount(Math.ceil(response.data.count / pageSize));
            setFTCurrentPage(value);
        } catch (error) {
            dispatch({ type: OPEN_ERROR_ALERT, payload: { message: "Something wrong happened! Or no more data!" } });
        }
    }
    return (
        <div style={{ overflow: "auto" }}>
            <Row className="head_table" style={{ minWidth: "950px" }}>
                <Col xs={5}>
                    <span>Token Name</span>
                </Col>
                <Col xs={2}>
                    <span>Symbol</span>
                </Col>
                <Col xs={2}>
                    <span>Standard</span>
                </Col>
                <Col xs={2}>
                    <span>Network Type</span>
                </Col>
                <Col xs={1} style={{ textAlign: "right" }}>
                    <span></span>
                </Col>
            </Row>
            {ftPageData.map((token, index) => {
                let token_type = ["ERC-20", "ERC-721"].includes(token.token_standard) ? "fungible" : "non_fungible";
                return (
                    <Row key={"token" + index + token?.token_name} className="card_list_view_mode" style={{ minWidth: "950px" }}>
                        <Col xs={5} className="card_list_view_mode_name">
                            <span className="card_list_view_mode_icon">
                                <img src={token.token_icon ? token.token_icon : imagePath.TOKEN_DEFAULT} style={{ borderRadius: "50%", objectFit: "cover" }} width={30} height={30} alt="" />
                            </span>
                            <span style={{ fontWeight: "bold" }}>{token?.token_name || "Unknow"}</span>
                        </Col>
                        <Col xs={2}>
                            <span className="card_list_view_mode_data">{token?.token_symbol || "---"}</span>
                        </Col>
                        <Col xs={2}>
                            <span className="card_list_view_mode_data">{token?.token_standard || "---"}</span>
                        </Col>
                        <Col xs={2}>
                            <span className="card_list_view_mode_data">{token?.user_defined_network ? "Fabric" : "Ethereum"}</span>
                        </Col>
                        <Col xs={1} style={{ textAlign: "right" }}>
                            <CustomDropdown token={token} token_type={token_type} />
                        </Col>
                    </Row>
                );
            })}
            <br />
            <Pagination count={ftPageCount} page={ftCurrentPage} onChange={handleChangePage} color="primary" shape="rounded" variant="outlined" style={{ textAlign: "center" }} />
        </div>
    );
};

export default CardToken;
