import { TextField } from '@material-ui/core';
import React, { FC, useState , useEffect} from 'react';
import '../styles/Purchase.scss';

type PurchaseProps = {


};

const Purchase: FC<PurchaseProps> = () => {
	

	return (
        <form  noValidate autoComplete="on">
            <div className="formDiv">
                <TextField 
                    required 
                    id="standard-required" 
                    label="Credit Number" 
                    defaultValue=""
                />
                <TextField 
                    required 
                    id="standard-required" 
                    label="Address" 
                    defaultValue=""
                />
                <TextField 
                    required 
                    id="standard-required" 
                    label="Age" 
                    defaultValue=""
                />
            </div>
            <button>
                Check
            </button>
        </form>
	);
};

export default Purchase;
