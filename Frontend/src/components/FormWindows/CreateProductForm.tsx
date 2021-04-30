import React, { FC, useState } from 'react';

import { TextField } from '@material-ui/core';
import FormWindow from './FormWindow';

type CreateProductFormProps = {
	onSubmit: (name: string, price: number, quantity: number, category: string) => void;
};

const CreateProductForm: FC<CreateProductFormProps> = ({ onSubmit }) => {
	const [name, setName] = useState<string>('');
	const [price, setPrice] = useState<string>('');
	const [quantity, setQuantity] = useState<string>('');
	const [category, setCategory] = useState<string>('');
	const [priceError, setPriceError] = useState<boolean>(false);
	const [quantityError, setQuantityError] = useState<boolean>(false);

	function handleSubmit() {
		const isNumeric = (value: string): boolean => !isNaN(+value);
		setPriceError(!isNumeric(price) || +price < 0);
		setQuantityError(!isNumeric(quantity) || +quantity < 0);
		if (!priceError && !quantityError) {
			onSubmit(name, +price, +quantity, category);
		}
	}
	return (
		<FormWindow createText="Add Product!" handleSubmit={handleSubmit} header="New product">
			<TextField
				required
				margin="normal"
				id="name"
				fullWidth
				label="Product's name"
				onChange={(event) => setName(event.currentTarget.value)}
			/>
			<TextField
				required
				margin="normal"
				id="price"
				fullWidth
				label="Product's price"
				onChange={(event) => setPrice(event.currentTarget.value)}
				inputMode="decimal"
				error={priceError}
			/>
			<TextField
				required
				margin="normal"
				id="quantity"
				fullWidth
				label="Product's quantity"
				onChange={(event) => setQuantity(event.currentTarget.value)}
				inputMode="numeric"
				type="number"
				error={quantityError}
			/>
			<TextField
				required
				margin="normal"
				id="category"
				fullWidth
				label="Product's category"
				onChange={(event) => setCategory(event.currentTarget.value)}
			/>
		</FormWindow>
	);
};

export default CreateProductForm;
