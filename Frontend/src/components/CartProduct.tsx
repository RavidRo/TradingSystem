import React, { FC, useState } from 'react';
import { IconButton } from '@material-ui/core';
import CancelIcon from '@material-ui/icons/Close';

import IncrementField from './IncrementField';
import { Product } from '../types';

type CartProductProps = {
	product: Product;
	onRemove: (id: string) => void;
	onChangeQuantity: (id: string, newQuantity: number) => void;
};

const digitPointPrecision = 3;

const CartProduct: FC<CartProductProps> = ({ product, onRemove, onChangeQuantity }) => {
	const { id, name, price, quantity: initialQuantity } = product;
	const [quantity, setQuantity] = useState<number>(initialQuantity);
	return (
		<div className="product">
			<div className="product-fields">
				<p className="name">{name}</p>
				<IncrementField
					onChange={(newQuantity) => {
						setQuantity(newQuantity);
						onChangeQuantity(id, newQuantity);
					}}
					value={quantity}
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
