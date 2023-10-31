import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import Modal from 'react-bootstrap/Modal'
import { Button } from 'react-bootstrap'
import { Form, Badge } from 'react-bootstrap'


import { getTokenDetail, getFTTokens } from 'src/services/User/tokens';
import { addLinkToken } from 'src/services/User/tokens'

const AddLinkModal = (props) => {
    const pageSize=10
    const [tokens_to_add, setTokensToAdd] = useState([])
    const [ftCurrentPage, setFTCurrentPage] = useState(1)
    const [ftPageCount, setFTPageCount] = useState(1)
    const [token, setToken] = useState([])
    useEffect(async () => {
        try {
            let response = await getFTTokens({page: ftCurrentPage})
            setTokensToAdd(response.data.results)
            setFTPageCount(Math.ceil(response.data.count/pageSize))
        } catch (error) {
            alert("Something wrong happened. Please reload the page.");
        }
    }, [])
    const handleClose=props.handleClose

    function handleTokenChange(e){
        setToken(e.target.value)
    }
    function handleSaveChangeClick() {
        addLinkToken({fromToken: props.currentToken, toToken: token}).then(
            res => window.location.reload()).catch(
                err => {alert("Something wrong happened. Please reload the page.");}
            )
        return handleClose
    }

    return(
        <>
        <Modal centered={true} show={props.show} onHide={props.handleClose} animation={false}>
            <Modal.Header closeButton>
                <Modal.Title>Link Token</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form.Control as="select" value={token ? token.name : ''} onChange={handleTokenChange}>
                    <option value=''>Select Token</option>
                    {tokens_to_add.map(token => <option data-value={token} value={token.id} key={token.id}>{token.token_name}</option>)}
                </Form.Control>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={props.handleClose}>
                    Cancel
                </Button>
                <Button variant="primary" onClick={handleSaveChangeClick}>
                    Save Changes
                </Button>
            </Modal.Footer>
      </Modal>
    </>
    )

}

export default AddLinkModal