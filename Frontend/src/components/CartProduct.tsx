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
};

const digitPointPrecision = 3;

const CartProduct: FC<CartProductProps> = ({ product,quantity, onRemove, onChangeQuantity }) => {
	const { id, name, price } = product;
	const [quantityMy, setQuantity] = useState<number>(quantity);
	return (
		<div className="product">
			<div className="product-fields">
				<p className="name">{name}</p>
				<IncrementField
					onChange={(newQuantity) => {
						setQuantity(newQuantity);
						onChangeQuantity(id, newQuantity);
					}}
					value={quantityMy}
					
				/>
				<p className="price">${price.toPrecision(digitPointPrecision)}</p>
			</div>
			<IconButton aria-label="remove" onClick={() => onRemove(id)}>
				<CancelIcon />
			</IconButton>
		</div>
	);
};

export default CartProduct;
