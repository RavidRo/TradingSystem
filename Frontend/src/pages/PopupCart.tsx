
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@material-ui/core';
import React ,{FC} from 'react';
import '../styles/PopupCart.scss';
import ProductPopup from './ProductPopup';

type PopupCartProps = {
    content: string,
   
};
const PopupCart: FC<PopupCartProps> = ({content}: PopupCartProps) => {

    let products = ['milk','coffee','shirt','suit'];

	return (
		
		<div className="popupCart">
            
            <TableContainer>
                <Table  aria-label="simple table">
                    <TableHead className="tableHead">
                    <TableRow>
                        <TableCell align={'center'}>Product</TableCell>
                        <TableCell align={'center'}>Quantity</TableCell>
                        <TableCell></TableCell>
                    </TableRow>
                    </TableHead>
                    <TableBody>
                        {products.map((p) => (
                            <ProductPopup
                            name={p}
                            quantity = {1}
                            key={p}
                            />
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
            
		</div>
	);
}

export default PopupCart;
