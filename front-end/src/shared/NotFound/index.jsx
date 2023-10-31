import React, { Fragment, useState, useEffect } from 'react';
import { Box, Container } from '@material-ui/core';
import Img from 'src/assets/images/page_not_found.svg'

const NotFound = (props) => {
    return (
        <Fragment>
            <Box display="flex" flexDirection="column" justifyContent="center">
                <Container maxWidth="lg">
                    <Box textAlign="center">
                        <img src={require({Img})} alt='notfound'/>
                    </Box>
                </Container>
            </Box>
        </Fragment>
    )
}

export default NotFound