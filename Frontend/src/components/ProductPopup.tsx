
import { TableCell, TableRow } from '@material-ui/core';
import React ,{FC, useEffect, useState} from 'react';
import '../styles/ProductPopup.scss';
import {Product} from '../types';

type ProductPopupProps = {
    id:string,
    name:string,
    price:number,
    quantity: number,
    keywords:string[],
    category:string,
    propHandleDelete:(product:Product)=>Promise<boolean> | boolean,
    changeQuantity:(productID:string,newQuantity:number)=>Promise<boolean>,
   
};
const PopupCart: FC<ProductPopupProps> = ({id,name,price,quantity,keywords,category,propHandleDelete,changeQuantity}: ProductPopupProps) => {

const [prod_quantity, setQuantity] = useState<number>(quantity);
useEffect(()=>{
    setQuantity(quantity);
},[quantity]);

//every time the - is pressed
const handleDelete = ()=>{
    if(prod_quantity===1){ // need to remove 
        propHandleDelete({id:id, name:name, price:price, keywords:keywords, category:category});
        setQuantity(0);
    }
    else{ // need to change quantity
        let answer = changeQuantity(id,prod_quantity - 1);
        answer.then((result)=>{
            if(result===true){
                setQuantity(prod_quantity-1);
            }
        })
    }
}
//every time the + is pressed
const handleAddPoup = ()=>{
    let answer = changeQuantity(id, prod_quantity + 1);
    answer.then((result)=>{
        if(result === true){
            setQuantity(prod_quantity + 1);
        }
        else{
            setQuantity(prod_quantity);
        }
    })
}

	return (
            prod_quantity>0?
                <TableRow style={{'alignItems':'right'}} >
                    <TableCell align={'center'}>{name}</TableCell>
                    <TableCell align={'center'}>{price*prod_quantity}</TableCell>
                    <TableCell align={'center'}>{prod_quantity}</TableCell>
                    <TableCell className="buttonsCell" >
                        <div className="buttons">
                            <button className="buttonP" onClick={()=>handleAddPoup()}>
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
