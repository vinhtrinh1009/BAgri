import React, { useEffect, useState, useRef } from "react";
import { Container, Row, Col, Card, CardHeader, CardBody } from 'reactstrap';
import { TextField, MenuItem, Button, FormControl, InputLabel, Select, Box, LinearProgress } from '@mui/material'; 
import { getContractInterface, getFTTokens, getTokenDetail } from "src/services/User/tokens";
import { ViewFunctionForm } from './components';

const InspectTokenPage = () => {
    const pageSize = 10
    const [tokens, setTokens] = useState([])
    const [ftCurrentPage, setFTCurrentPage] = useState(1)
    const [ftPageCount, setFTPageCount] = useState(1)
    const [token, setToken] = useState('');
    const [totalSupplyArgument, setTotalSupplyArgument] = useState(undefined);
    const [loading, setLoading] = useState(false);

    const [contractInterface, setContractInterface] = useState(undefined);
    const [viewFunctions, setViewFunctions] = useState([]);

    useEffect(async () => {
        try {
            let response = await getFTTokens({page: ftCurrentPage});
            const res = response.data.results;

            setTokens(res);

            // DEBUG
            if(tokens) setToken(res[0]);

            setFTPageCount(Math.ceil(response.data.count/pageSize));
        } catch (error) {
            alert("Something wrong happened. Please reload the page.");
        }
    }, [])

    useEffect(() => {
        if(!token) return;

        getTokenDetail({token_type: 'fungible', token_id: token.id}).then(res => {
            // DEBUG
            console.log('token', token);

            if(res.network){
                // query inside backend
            }
            else{
                // TODO: Dungld implement this case
            }


            getContractInterface({url: res.data.abi}).then(res2 => {
                setContractInterface(res2.data);
                setLoading(false);
            }).catch(e => {
                alert("Unable to get token interface. Please try again");
                setLoading(false);
            })
        }).catch(e => {
            alert("Unable to get token detail. Please try again");
            setLoading(false);
        })
    }, [token])

    useEffect(() => {
        if(!contractInterface){
            setViewFunctions([]);
            return;
        }

        let functions = [];

        for (let i=0; i<contractInterface.length; i++) {
            if (contractInterface[i].type === 'function' && contractInterface[i].stateMutability === 'view') {
                functions.push(contractInterface[i]);
            }
        }

        console.log(functions);

        setViewFunctions(functions);
    }, [contractInterface])
    
    const handleTokenChange = (e) => {
        setToken(e.target.value);
        setLoading(true);
    }

    function handleTotalSupplyArgumentChange(e){

    }

    function handleGetTotalSupplyClick() {

    }
    
    function handleGetBalanceClick() {

    }

    return (
        <>
            <Container style={{ maxWidth: "1605px", margin: "0px auto", paddingTop: "30px" }}>
                <Row>
                    <Col sm={4} style={{ display: "flex", alignItems: "center", justifyContent: "left" }}>
                        <strong style={{ font: "normal normal bold 24px/28px Roboto"}}>Inspect Token</strong>
                    </Col>
                    <Col sm={8} style={{ display: "flex", alignItems: "center", justifyContent: "right" }}>
                       
                    </Col>
                </Row>

                <Row>
                    <Col className="box-col-12">
                        <Card style={{ minHeight: "583px", marginTop: "2%" }}>
                            <CardBody style={{ padding: "80px 30px 110px 30px" }}>
                                <div className="container">
                                    <Row>
                                        <Col className="col">
                                            <h6>Token</h6>
                                            <FormControl variant="filled" fullWidth required size="small">
                                                <InputLabel id="from-token">Select token</InputLabel>

                                                <Select labelId="from-token" onChange={handleTokenChange} value={token} defaultValue={''}>
                                                    {tokens.map(token => (
                                                        <MenuItem key={token.id} value={token}>{token.token_name}</MenuItem>
                                                    ))}
                                                </Select>
                                            </FormControl>
                                        </Col>
                                    </Row>
                                    
                                    <div className="mt-5 d-flex flex-column">
                                        {viewFunctions.map((func, i) => <ViewFunctionForm key={i} token={token} func={func} index={i} className="mb-2"/>)}
                                    </div>
                                </div>
                            </CardBody>
                        </Card>
                    </Col>
                </Row>
            </Container>
        </>
    )
}

export default InspectTokenPage