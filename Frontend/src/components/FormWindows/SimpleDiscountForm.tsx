import React, { FC } from 'react';

import { FormControl, InputLabel, MenuItem, Select, TextField } from '@material-ui/core';
import { DiscountObject, DiscountSimple, Product } from '../../types';

type SimpleDiscountFormProps = {
	setPercentage: (percentage: string) => void;
	percentageError: boolean;
	contextObject: DiscountObject | '';
	setContextObject: (object: DiscountObject) => void;
	contextIdentifier: string;
	setContextIdentifier: (identifier: string) => void;
	products: Product[];
	defaultDiscount?: DiscountSimple;
};

const SimpleDiscountForm: FC<SimpleDiscountFormProps> = ({
	setPercentage,
	percentageError,
	contextObject,
	setContextObject,
	contextIdentifier,
	setContextIdentifier,
	products,
	defaultDiscount,
}) => {
	const handleObjectChange = (event: React.ChangeEvent<{ value: unknown }>) => {
		setContextObject(event.target.value as DiscountObject);
	};
	const handleIdentifierChange = (event: React.ChangeEvent<{ value: unknown }>) => {
		setContextIdentifier(event.target.value as string);
	};

	const categories = Array.from(new Set(products.map((product) => product.category)));

	return (
		<>
			<TextField
				required
				margin="normal"
				id="percentage"
				fullWidth
				label="Percentage"
				onChange={(event) => setPercentage(event.currentTarget.value)}
				inputMode="numeric"
				type="number"
				error={percentageError}
				defaultValue={`${defaultDiscount?.percentage || ''}`}
			/>
			<FormControl fullWidth margin="normal">
				<InputLabel id="object-label">Context</InputLabel>
				<Select
					labelId="object-label"
					id="object-select"
					value={contextObject}
					onChange={handleObjectChange}
					required
					defaultValue={defaultDiscount?.context.obj || ''}
				>
					<MenuItem value={'product'}>Product</MenuItem>
					<MenuItem value={'category'}>Category</MenuItem>
					<MenuItem value={'store'}>Store</MenuItem>
				</Select>
			</FormControl>
			{contextObject !== 'store' && contextObject !== '' && (
				<FormControl fullWidth margin="normal">
					<InputLabel id="identifier-label">Identifier</InputLabel>
					<Select
						labelId="identifier-label"
						id="identifier-select"
						value={contextIdentifier}
						onChange={handleIdentifierChange}
						required
						defaultValue={
							(defaultDiscount?.context.obj !== 'store' &&
								defaultDiscount?.context?.id) ||
							''
						}
					>
						{contextObject === 'category'
							? categories.map((category, index) => (
									<MenuItem key={index} value={category}>
										{category}
									</MenuItem>
							  ))
							: products.map((product, index) => (
									<MenuItem key={index} value={product.id}>
										{product.name}
									</MenuItem>
							  ))}
					</Select>
				</FormControl>
			)}
		</>
	);
};

export default SimpleDiscountForm;
