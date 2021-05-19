import { Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, TextField } from '@material-ui/core';
import React ,{FC, useEffect, useState,useRef} from 'react';
import '../styles/OfferField.scss';


type OfferFieldProps = {
    offer:number,
};

const OfferField: FC<OfferFieldProps> = ({offer}) => {

    const [currentOffer,setOffer] = useState<number>(offer);

    const [newOffer, setNewOffer] = useState<number>(0);

    const [open, setOpen] = useState<boolean>(false);
    
    const handleClickChange = ()=>{
        setOpen(true);
    }
    const changeOffer = (e:number)=>{
        setNewOffer(e);
    }
    //just when the user agrees, the current offer changes
    const handleOk = ()=>{
        setOffer(newOffer);
        setOpen(false);
    }
    return (
		
		<div className="offerDiv">
            <p>{currentOffer}</p>
            <button className="offerBtn" onClick={handleClickChange}>Change Offer</button>
            <Dialog open={open} onClose={()=>setOpen(false)} aria-labelledby="form-dialog-title">
                <DialogTitle  id="form-dialog-title">Enter Your Offer</DialogTitle>
                <DialogContent>
                <DialogContentText style={{'fontSize':'20px','color':'black'}}>
                    Enter the price you want to offer on the item
                </DialogContentText>
                <TextField
                    autoFocus
                    margin="dense"
                    id="offer"
                    label="offer"
                    type="number"
                    fullWidth
                    onChange={(e)=>changeOffer(+e.target.value)}
                />
                </DialogContent>
                <DialogActions>
                <Button style={{'color':'blue'}} onClick={()=>setOpen(false)} >
                    Cancel
                </Button>
                <Button style={{'color':'blue'}} onClick={()=>handleOk()}>
                    Offer
                </Button>
                </DialogActions>
            </Dialog>
		</div>
	);
}

export default OfferField;
