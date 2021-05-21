import React, { FC, useState, useRef } from 'react';
import { IconButton, MenuItem, Select } from '@material-ui/core';
import CancelIcon from '@material-ui/icons/Close';

import IncrementField from './IncrementField';
import { Product } from '../types';
import '../styles/CardProduct.scss';
import OfferField from '../components/OfferField';

type CartProductProps = {
	product: Product;
	quantity: number;
	onRemove: (product: Product) => void;
	propHandleAdd: (product: Product) => Promise<boolean>; //to update server
	changeQuantity: (productID: string, newQuantity: number) => Promise<boolean>; //to update bag and total amount in cart
};

const CartProduct: FC<CartProductProps> = ({
	product,
	quantity,
	onRemove,
	propHandleAdd,
	changeQuantity,
}) => {
	const { id, name, price } = product;
	const [quantityMy, setQuantity] = useState<number>(quantity);

	const purchaseTypes = useRef<string[]>(['immediate', 'offer']);
	const [currentType, setCurrentType] = useState<string>('immediate');

	const handleAdd = () => {
		let me = product;
		//calling the server to add product to cart
		let answer = propHandleAdd(me);
		answer.then((result) => {
			if (result === true) {
				setQuantity(quantityMy + 1);
			}
		});
	};
	// when - is presses , only decrease product  not remove
	const handleDelete = () => {
		let answer = changeQuantity(id, quantityMy - 1); //update bag
		answer.then((result) => {
			if (result === true) {
				setQuantity(quantityMy - 1);
			}
		});
	};
	const handleChangeQuantity = (newQuantity: number) => {
		if (newQuantity > quantityMy) {
			handleAdd();
		} else {
			handleDelete();
		}
	};
	const handleChangeType = (e: any) => {
		setCurrentType(e.target.value);
	};
	return quantityMy > 0 ? (
		<div className='product'>
			<div className='product-fields'>
				<p className='name'>{name}</p>
				<IncrementField
					onChange={(newQuantity) => handleChangeQuantity(newQuantity)}
					value={quantityMy}
				/>
				<p className='price'>${price}</p>
			</div>

			<IconButton aria-label='remove' onClick={() => onRemove(product)}>
				<CancelIcon />
			</IconButton>
			<Select
				style={{ fontSize: '1rem', width: '30%' }}
				value={currentType}
				onChange={(e) => handleChangeType(e)}
			>
				{purchaseTypes.current.map((type) => {
					return (
						<MenuItem value={type} key={purchaseTypes.current.indexOf(type)}>
							{type}
						</MenuItem>
					);
				})}
			</Select>
			{currentType === 'offer' ? (
				//TODO: should be offer value from server
				<OfferField offer={0} />
			) : null}
		</div>
	) : null;
};

export default CartProduct;
