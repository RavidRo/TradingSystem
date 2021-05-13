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
	onChangeQuantity: (id: string, newQuantity: number) => void;
	propHandleAdd:(product:Product)=>Promise<boolean>,
    propHandleDelete:(productID:string)=>void,
    changeQuantity:(productID:string,newQuantity:number)=>void,

};

const digitPointPrecision = 3;



const CartProduct: FC<CartProductProps> = ({ product,quantity, onRemove, onChangeQuantity,propHandleAdd,propHandleDelete ,changeQuantity}) => {
	const { id, name, price } = product;
	const [quantityMy, setQuantity] = useState<number>(quantity);

	const handleAdd = ()=>{
		let me = product;
		let answer = propHandleAdd(me);
		answer.then((result)=>{
			if(result === true){
				setQuantity(quantityMy + 1);
			}
			else{
				setQuantity(quantityMy);
			}
		})
	}

	const handleDelete = ()=>{
		if(quantityMy===1){
			propHandleDelete(id);
			setQuantity(0);
		}
		else{
			setQuantity(quantityMy-1);
			changeQuantity(id,quantityMy - 1);
		}
	}
	const handleChangeQuantity = (newQuantity:number)=>{
		if(newQuantity > quantityMy){
			handleAdd();
			onChangeQuantity(id, newQuantity);
		}
		else{
			handleDelete();
			onChangeQuantity(id, newQuantity);
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
					<p className="price">${price.toPrecision(digitPointPrecision)}</p>
				</div>
				<IconButton aria-label="remove" onClick={() => onRemove(id)}>
					<CancelIcon />
				</IconButton>
			</div>
		:null
	);
};

export default CartProduct;
