
import { TableCell, TableRow } from '@material-ui/core';
import React ,{FC, useState} from 'react';
import '../styles/ProductPopup.scss';


type ProductPopupProps = {
    name:string,
    quantity: number
   
};
const PopupCart: FC<ProductPopupProps> = ({name,quantity}: ProductPopupProps) => {
const [prod_quantity, setQuantity] = useState<number>(quantity);

	return (
		
        <TableRow >
            <TableCell>{name}</TableCell>
            <TableCell >{prod_quantity}</TableCell>
            <TableCell className="buttonsCell" >
                <button className="buttonP" onClick={()=>setQuantity(prod_quantity+1)}>
                    +
                </button>
                <button className="buttonM" onClick={()=>setQuantity(prod_quantity-1)}>
                    -
                </button>
            </TableCell>
        </TableRow>
	);
}

export default PopupCart;
