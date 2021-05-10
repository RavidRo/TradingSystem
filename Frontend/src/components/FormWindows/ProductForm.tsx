import React, { FC, useRef, useState } from 'react';

import { Chip, Fab, TextField } from '@material-ui/core';
import AddIcon from '@material-ui/icons/Add';

import FormWindow from './FormWindow';
import { ProductQuantity } from '../../types';

type ProductFormProps = {
	onSubmit: (
		name: string,
		price: number,
		quantity: number,
		category: string,
		keywords: string[]
	) => void;
	productEditing?: ProductQuantity;
};

const ProductForm: FC<ProductFormProps> = ({ onSubmit, productEditing = undefined }) => {
	const [name, setName] = useState<string>(productEditing ? `${productEditing.name}` : '');
	const [price, setPrice] = useState<string>(productEditing ? `${productEditing.price}` : '');
	const [quantity, setQuantity] = useState<string>(
		productEditing ? `${productEditing.quantity}` : ''
	);
	const [category, setCategory] = useState<string>(productEditing ? productEditing.category : '');
	const [keywords, setKeywords] = useState<string[]>(
		productEditing ? productEditing.keywords : []
	);

	const currentKeyword = useRef<HTMLInputElement>(null);

	const [priceError, setPriceError] = useState<boolean>(false);
	const [quantityError, setQuantityError] = useState<boolean>(false);

	function handleSubmit() {
		const isNumeric = (value: string): boolean => !isNaN(+value);
		setPriceError(!isNumeric(price) || +price < 0);
		setQuantityError(!isNumeric(quantity) || +quantity < 0);
		if (!priceError && !quantityError) {
			onSubmit(name, +price, +quantity, category, keywords);
		}
	}
	return (
		<FormWindow
			createText={productEditing ? 'Edit Product' : 'Add Product!'}
			handleSubmit={handleSubmit}
			header={productEditing ? 'Confirm' : 'New product'}
		>
			<TextField
				required
				margin="normal"
				id="name"
				fullWidth
				label="Product's name"
				onChange={(event) => setName(event.currentTarget.value)}
				defaultValue={productEditing?.name}
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
				defaultValue={productEditing?.price}
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
				defaultValue={productEditing?.quantity}
			/>
			<TextField
				required
				margin="normal"
				id="category"
				fullWidth
				label="Product's category"
				onChange={(event) => setCategory(event.currentTarget.value)}
				defaultValue={productEditing?.category}
			/>
			<div className="enter-keywords">
				<div className="keyword-input">
					<TextField
						margin="normal"
						id="keyword"
						label="Keyword"
						fullWidth
						inputRef={currentKeyword}
					/>
				</div>
				<Fab
					color="primary"
					aria-label="add"
					onClick={() => {
						if (currentKeyword.current && currentKeyword.current.value !== '') {
							console.log(currentKeyword.current);
							setKeywords([currentKeyword.current.value, ...keywords]);
							currentKeyword.current.value = '';
							currentKeyword.current.focus();
						}
					}}
					size="small"
				>
					<AddIcon />
				</Fab>
			</div>
			{keywords.length > 0 && (
				<div>
					{keywords.map((keyword) => (
						<Chip
							label={keyword}
							onDelete={() =>
								setKeywords(keywords.filter((current) => current !== keyword))
							}
						/>
					))}
				</div>
			)}
		</FormWindow>
	);
};

export default ProductForm;
