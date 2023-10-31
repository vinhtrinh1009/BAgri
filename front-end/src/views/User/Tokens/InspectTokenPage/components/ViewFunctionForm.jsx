import React, { useEffect, useState, useRef } from 'react';

import ArrowRightIcon from '@mui/icons-material/ArrowRight';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import IconButton from '@mui/material/IconButton';
import { Button, TextField, LinearProgress } from '@mui/material';
import { inspectToken } from 'src/services/User/tokens';

export const ViewFunctionForm = ({ token, func, index, style, className }) => {
    const [open, setOpen] = useState(true);
    const [loading, setLoading] = useState(false);
    const [outputs, setOutputs] = useState([]);
    const inputMap = useRef(new Map());

    useEffect(() => {
        for (let i=0; i<func.inputs.length; i++) {
            inputMap.current.set(i, '');
        }
    }, [])

    const handleToggle = () => {
        setOpen(!open);
    }

    useEffect(() => {
        // inspect function with 0 input

        if(!open || outputs.length !== 0) return;
       
        if(func.inputs.length > 0) return;

        triggerInspectToken();
    }, [open])

    const handleQuery = () => {
        triggerInspectToken();
    }

    const triggerInspectToken = () => {
        setLoading(true);
        inspectToken({token_id: token.id, func: func, input_map: inputMap.current}).then(res => {
            setOutputs(res.data);
            setLoading(false);
        }).catch(e => {
            setLoading(false);
            console.error('loi roi ban oi', func);
        })
    }

    return (
        <div style={{...style, border: '1px solid lightgray', borderRadius: '2px', overflow: 'hidden'}} className={className}>
            <a type="button" className="w-100" onClick={handleToggle}>
                <div className="d-flex w-100 align-items-center justify-content-between p-2" style={{backgroundColor: 'rgb(244, 247, 250)'}}>
                    {`${index+1}. ${func.name}`}

                    {open && <ArrowDropDownIcon/>}
                    {!open && <ArrowRightIcon/>}
                </div>
            </a>

            {open &&
            <div className="p-3">

                {func.inputs.length !== 0 && 
                <>
                <div className="d-flex flex-column">
                    {func.inputs.map((input, i) => 
                    <TextField key={i} value={inputMap.current.get(i)} onChange={(e) => {inputMap.current.set(i, e.target.value)}} variant="outlined" label={`${input.name} (${input.type})`} fullWidth className="mb-4" size='small'></TextField>
                    )}
                </div>
                <Button variant='contained' size='small' style={{backgroundColor: 'rgb(224, 227, 230)', color: 'black'}} onClick={handleQuery} disabled={loading}>Query</Button>
                </>
                }

                {outputs.map((output, i) => 
                <div key={i}>
                    <span>{output.value.toString()}</span>{' '}<span style={{fontStyle: 'italic', color: 'gray'}}>{output.type}</span>
                </div>
                )}

                {loading && <LinearProgress/>}
            </div>
            }
            
        </div>
        
    )
};
