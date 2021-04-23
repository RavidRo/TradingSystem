
import { TableCell, TableRow } from '@material-ui/core';
import { triggerAsyncId } from 'node:async_hooks';
import React ,{FC} from 'react';
import '../styles/ProductPopup.scss';


type ProductPopupProps = {
    name:string,
    quantity: number
   
};
const PopupCart: FC<ProductPopupProps> = ({name,quantity}: ProductPopupProps) => {


	return (
		
        <TableRow >
            <TableCell>{name}</TableCell>
            <TableCell >{quantity}</TableCell>
            <TableCell className="buttonsCell" >
                <button className="buttonP">
                    +
                </button>
                <button className="buttonM">
                    -
                </button>
            </TableCell>
        </TableRow>
	);
}

export default PopupCart;
