
import { TableCell, TableRow } from '@material-ui/core';
import React ,{FC, useState} from 'react';
import '../styles/ProductPopup.scss';
import {Product,ProductQuantity} from '../types';

type ProductPopupProps = {
    id:string,
    name:string,
    price:number,
    quantity: number,
    keywords:string[],
    category:string,
    propHandleDelete:(product:ProductQuantity)=>void,
   
};
const PopupCart: FC<ProductPopupProps> = ({id,name,price,quantity,keywords,category,propHandleDelete}: ProductPopupProps) => {
const [prod_quantity, setQuantity] = useState<number>(quantity);
const handleDelete = ()=>{
    if(prod_quantity===1){
        propHandleDelete({id:id,name:name,price:price,quantity:quantity,keywords:keywords,category:category});
        setQuantity(0);
    }
    else{
        setQuantity(prod_quantity-1);
    }
}
	return (
            prod_quantity>0?
                <TableRow style={{'alignItems':'right'}} >
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
            :null
	);
}

export default PopupCart;
