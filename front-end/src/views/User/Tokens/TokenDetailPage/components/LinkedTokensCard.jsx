import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux'
import avatar_placeholder from "../../../../../assets/images/user/7.jpg";
import { Row, Col, Container, Card, CardHeader, CardFooter, CardBody, Table, Input } from 'reactstrap';
import { PlusSquare } from 'react-feather';
import { Link } from "react-router-dom";
import { useLocation, useParams } from 'react-router';
import { getTokenDetail, getLinkedToken, unlinkTokens } from 'src/services/User/tokens';
import AddLinkModal from './AddLinkModal';
import Button from '@mui/material/Button';
import AddBoxOutlinedIcon from '@mui/icons-material/AddBoxOutlined';

const LinkedTokensCard = (props) => {
    const linked_contract = props.linked_contract
    const [linked_tokens, setLinkedTokens] = useState([{}])
    const [delete_linked_tokens, setDeleteLinkedTokens] = useState([])
    const [buttonClicked, setButtonClicked] = useState(false)
    function handleAddButtonClick(){
        setButtonClicked(true)
    }
    function handleClose(){
        setButtonClicked(false)
    }
    function handleDeleteButtonClick(){
        unlinkTokens({fromToken: linked_contract, toToken: delete_linked_tokens})
        .then(res => {
            window.location.reload()
        }).catch(err => {
            alert("Something wrong happened. Please try again later")
        })
    }

    function handleTokenSelect(e){
        const deletingTokenId = e.target.value
        let newDelLinkTokens = delete_linked_tokens
        newDelLinkTokens.push(deletingTokenId)
        setDeleteLinkedTokens(newDelLinkTokens)
    }

    useEffect(async () => {
        getLinkedToken({linked_contract: linked_contract}).then(res => {
            setLinkedTokens(res.data.results)
        }).catch(err => {
            alert("Something wrong happened. Please reload the page.");
        })
    }, [])

    return (
        <>  
            <AddLinkModal currentToken={linked_contract} handleShow={handleAddButtonClick} handleClose={handleClose} show={buttonClicked}/>

            <Card style={{ marginTop: '2%' }}>
                <CardHeader style={{ display: 'inline-flex', alignItems: 'center' }}>
                    <h5>Linked to</h5>
                    <div className="media-body text-right">
                        <Button variant="contained" onClick={handleAddButtonClick} startIcon={<AddBoxOutlinedIcon/>}>
                            Add link
                        </Button>
                    </div>
                </CardHeader>

                <CardBody >
                    <Row>
                    <Table hover borderless responsive>
                        <thead>
                            <tr>
                                <th>Token name</th>
                                <th>Network</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            {linked_tokens.map((token, index) => {
                                let token_type = ['ERC-20', 'ERC-721'].includes(token.token_standard) ? 'fungible' : 'non_fungible'
                                return (
                                    <tr key={index}>
                                        <td>
                                            {/* <Link to={{
                                                    pathname: `/user/tokens/${token.id}/${token_type}`,
                                                }} 
                                                // className="btn" 
                                                style={{ display: 'inline-flex', alignItems: 'top' }}
                                                onClick={() => {window.location.reload()}}
                                            > */}
                                                {token.token_name}

                                            {/* </Link> */}
                                        </td>
                                        <td>
                                            {}
                                        </td>
                                        <td>
                                            <div>
                                                <Input type="checkbox" defaultChecked={false} value={token.id} onChange={handleTokenSelect}/> 
                                            </div>
                                        </td>
                                    </tr>   
                                )
                            })}
                            
                        </tbody>
                    </Table>
                    </Row>
                </CardBody>
                <CardFooter style={{ display: 'inline-flex', alignItems: 'center' }}>                  
                    <div className="media-body text-right">
                        <Button
                            variant='contained'
                            color='error'
                            onClick={handleDeleteButtonClick}>
                            Deleted link
                        </Button>
                    </div>
                </CardFooter>
            </Card>
        </>
    )
}

export default LinkedTokensCard