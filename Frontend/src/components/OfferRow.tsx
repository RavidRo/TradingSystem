import { Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Table, TableBody, TableCell, TableHead, TableRow, TextField } from '@material-ui/core';
import React, { FC , useState} from 'react';
import Swal from 'sweetalert2';
import useAPI from '../hooks/useAPI';
import { Offer } from '../types';


type OffersRowProps = {
    offer: Offer,
};

const OffersRow: FC<OffersRowProps> = ({offer}) => {

	const [windowInput, setWindowInput] = useState<boolean>(false);
    const [offerInput, setOfferInput] = useState<number>(0);

    const handleDeclare = ()=>{
        setWindowInput(true);
    }
    const cancelOfferObj = useAPI<void>('/cancel_offer');
    const handleCancel = ()=>{
        cancelOfferObj.request({offer_id: offer.id}).then(({data, error})=>{
            if (!error && data) {
                Swal.fire({
					icon: 'success',
					title: 'Congratulations!',
					text: 'Your offer was canceled successfully!',
				});
            }
        })
    }
    const declareOfferObj = useAPI<void>('/declare_price');
    const handleOK = ()=>{
        setWindowInput(false);
        declareOfferObj.request({offer_id: offer.id, price: offerInput}).then(({data, error})=>{
            if (!error && data) {
                Swal.fire({
					icon: 'success',
					title: 'Congratulations!',
					text: 'Your offer was sent to the store manager, we will notify you when there will be an answer !',
				});
            }
        })
    }

return (
        <TableRow key={offer.id}>
            <TableCell component="th" scope="row">
                {offer.product_name}
            </TableCell>
            <TableCell component="th" scope="row">
                {offer.store_name}
            </TableCell>
            <TableCell component="th" scope="row">
                {offer.price}
            </TableCell>
            <TableCell component="th" scope="row">
                {offer.status}
            </TableCell>
            <TableCell component="th" scope="row">
                <button onClick={handleDeclare}>
                    Declare new price
                </button>
            </TableCell>
            <TableCell component="th" scope="row">
                <button onClick={handleCancel}>
                    Cancel Offer
                </button>
            </TableCell>

            <Dialog open={windowInput} onClose={() => setWindowInput(false)} aria-labelledby='form-dialog-title'>
				<DialogTitle id='form-dialog-title'>Enter Your Offer</DialogTitle>
				<DialogContent>
					<TextField
						autoFocus
						margin='dense'
						id='offer'
						label='Offer'
						type='number'
						fullWidth
						onChange={(e) => setOfferInput(+e.target.value)}
					/>
				</DialogContent>
				<DialogActions>
					<Button style={{ color: 'blue' }} onClick={() => setWindowInput(false)}>
						Cancel
					</Button>
					<Button style={{ color: 'blue' }} onClick={() => handleOK()}>
						OK
					</Button>
				</DialogActions>
			</Dialog>
        </TableRow>
	);
};


export default OffersRow;
