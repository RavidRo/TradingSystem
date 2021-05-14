import React, { FC, useState } from 'react';
import { IconButton } from '@material-ui/core';
import CancelIcon from '@material-ui/icons/Close';

import IncrementField from './IncrementField';
import { Product } from '../types';
import '../styles/CardProduct.scss';

type CartProductProps = {
	product: Product;
	quantity:number;
	onRemove: (id: string) => void;
	propHandleAdd:(product:Product)=>Promise<boolean>,//to update server
    propHandleDelete:(productID:string)=>void,//to update server
    changeQuantity:(productID:string,newQuantity:number)=>void,//to update bag and total amount in cart

};


const CartProduct: FC<CartProductProps> = ({ product,quantity, onRemove,propHandleAdd,propHandleDelete ,changeQuantity}) => {
	const { id, name, price } = product;
	const [quantityMy, setQuantity] = useState<number>(quantity);

	const handleAdd = ()=>{
		let me = product;
		//calling the server to add product to cart
		let answer = propHandleAdd(me);
		answer.then((result)=>{
			if(result === true){
				setQuantity(quantityMy + 1);
				changeQuantity(id,quantityMy + 1); //update bag
			}
			else{
				setQuantity(quantityMy);
			}
		})
	}

	const handleDelete = ()=>{
		if(quantityMy===1){
			propHandleDelete(id); //calling server to update cart
			setQuantity(0);
		}
		else{
			setQuantity(quantityMy-1);
			changeQuantity(id,quantityMy - 1);//update bag
		}
	}
	const handleChangeQuantity = (newQuantity:number)=>{
		if(newQuantity > quantityMy){
			handleAdd();
		}
		else{
			handleDelete();
		}
	}
	return (
		quantityMy > 0 ? 
			<div className="product">
				<div className="product-fields">
					<p className="name">{name}</p>
					<IncrementField
						onChange={(newQuantity) =>handleChangeQuantity(newQuantity)}
						value={quantityMy}
						
					/>
					<p className="price">${price}</p>
				</div>
				<IconButton aria-label="remove" onClick={() => onRemove(id)}>
					<CancelIcon />
				</IconButton>
			</div>
		:null
	);
};

export default CartProduct;
