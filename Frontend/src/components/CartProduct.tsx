import React, { FC, useState } from 'react';
import { IconButton } from '@material-ui/core';
import CancelIcon from '@material-ui/icons/Close';

import IncrementField from './IncrementField';
import { Product } from '../types';
import '../styles/CardProduct.scss';

type CartProductProps = {
	product: Product;
	quantity:number;
	onRemove: (product: Product) => void;
	propHandleAdd:(product:Product)=>Promise<boolean>,//to update server
    changeQuantity:(productID:string,newQuantity:number)=>Promise<boolean>,//to update bag and total amount in cart

};


const CartProduct: FC<CartProductProps> = ({ product,quantity, onRemove,propHandleAdd ,changeQuantity}) => {
	const { id, name, price } = product;
	const [quantityMy, setQuantity] = useState<number>(quantity);

	const handleAdd = ()=>{
		let me = product;
		//calling the server to add product to cart
		let answer = propHandleAdd(me);
		answer.then((result)=>{
			if(result === true){
				setQuantity(quantityMy + 1);
			}
		})
	}

	const handleDelete = ()=>{
			let answer = changeQuantity(id,quantityMy - 1);//update bag
			answer.then((result)=>{
				if(result===true){
					setQuantity(quantityMy-1);
				}
			})
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
				<IconButton aria-label="remove" onClick={() => onRemove(product)}>
					<CancelIcon />
				</IconButton>
			</div>
		:null
	);
};

export default CartProduct;
