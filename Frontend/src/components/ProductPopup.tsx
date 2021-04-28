
import { TableCell, TableRow } from '@material-ui/core';
import React ,{FC, useState} from 'react';
import '../styles/ProductPopup.scss';


type ProductPopupProps = {
    name:string,
    price:number,
    quantity: number,
    propHandleDelete:(product:{name:string,price:number})=>void,
   
};
const PopupCart: FC<ProductPopupProps> = ({name,price,quantity,propHandleDelete}: ProductPopupProps) => {
const [prod_quantity, setQuantity] = useState<number>(quantity);
const handleDelete = ()=>{
    if(prod_quantity===1){
        propHandleDelete({name:name,price:price});
    }
    setQuantity(prod_quantity-1);
}
	return (
		
        <TableRow >
            <TableCell align={'center'}>{name}</TableCell>
            <TableCell align={'center'}>{price*prod_quantity}</TableCell>
            <TableCell align={'center'}>{prod_quantity}</TableCell>
            <TableCell className="buttonsCell" >
                <div className="buttons">
                    <button className="buttonP" onClick={()=>setQuantity(prod_quantity+1)}>
                        +
                    </button>
                    <button className="buttonM" onClick={()=>handleDelete()}>
                        -
                    </button>
                </div>
            </TableCell>
        </TableRow>
	);
}

export default PopupCart;
