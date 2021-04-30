import React, { FC, useRef, useState } from 'react';

import { Chip, Fab, TextField } from '@material-ui/core';
import AddIcon from '@material-ui/icons/Add';

import FormWindow from './FormWindow';

type CreateProductFormProps = {
	onSubmit: (
		name: string,
		price: number,
		quantity: number,
		category: string,
		keywords: string[]
	) => void;
};

const CreateProductForm: FC<CreateProductFormProps> = ({ onSubmit }) => {
	const [name, setName] = useState<string>('');
	const [price, setPrice] = useState<string>('');
	const [quantity, setQuantity] = useState<string>('');
	const [category, setCategory] = useState<string>('');
	const [keywords, setKeywords] = useState<string[]>([]);

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

export default CreateProductForm;
