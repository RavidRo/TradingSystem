import { Chip } from '@material-ui/core';
import React, { FC } from 'react';
import { ProductQuantity } from '../../types';
import DetailsWindow from './DetailsWindow';

type ProductDetailsProps = {
	product: ProductQuantity;
};

const ProductDetails: FC<ProductDetailsProps> = ({ product }) => {
	const details = [
		{ field: 'Quantity', value: product.quantity.toString() },
		{ field: 'Price', value: product.price.toFixed(2) },
		{ field: 'Category', value: product.category },
	];
	return (
		<DetailsWindow header={`${product.name} - ${product.id}`} details={details}>
			{product.keywords.map((label, index) => (
				<Chip key={index} label={`#${label}`} variant="outlined" className="chip" />
			))}
		</DetailsWindow>
	);
};

export default ProductDetails;
