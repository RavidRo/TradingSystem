
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@material-ui/core';
import React ,{FC} from 'react';
import '../styles/PopupCart.scss';
import ProductPopup from './ProductPopup';

type PopupCartProps = {
    content: string,
   
};
const PopupCart: FC<PopupCartProps> = ({content}: PopupCartProps) => {

    let products = ['milk','coffee','shirt','milk','coffee','shirt','milk','coffee','shirt'];

	return (
		
		<div className="popupCart">
            
            <TableContainer>
                <Table  aria-label="simple table">
                    <TableHead>
                    <TableRow>
                        <TableCell>Product</TableCell>
                        <TableCell>Quantity</TableCell>
                        <TableCell></TableCell>
                    </TableRow>
                    </TableHead>
                    <TableBody>
                    {products.map((p) => (
                        <ProductPopup
                        name={p}
                        quantity = {1}
                        />
                    ))}
                    </TableBody>
                </Table>
            </TableContainer>
            
		</div>
	);
}

export default PopupCart;
