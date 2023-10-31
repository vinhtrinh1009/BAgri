import React, { Fragment, memo } from 'react';
import { Table } from 'reactstrap';
import { Handle } from 'react-flow-renderer';

export default memo(({ data, isConnectable }) => {
    return (
        <Fragment>
            <Handle
                type="target"
                position="left"
                id="a"
                style={{ background: '#555' }}
                onConnect={(params) => console.log('handle onConnect', params)}
                isConnectable={isConnectable}
            />
            <Table bordered style={{ width: "40px" }}>
                <tbody>
                    {
                        console.log(data)
                        // data.attributes.map((value, key) => {
                        //     console.log(value)
                        //     return (
                        //         <tr>
                        //             <th scope="row"></th>
                        //             <td>{value.name}</td>
                        //         </tr>
                        //     )
                        // })
                    }
                </tbody>
            </Table>
            <Handle
                type="source"
                position="right"
                id="b"
                style={{ background: '#555' }}
                isConnectable={isConnectable}
            />
        </Fragment>
    );
});