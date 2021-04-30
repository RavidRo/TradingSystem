import { Chip } from '@material-ui/core';
import React, { FC } from 'react';
import { Product } from '../../types';
import DetailsWindow from './DetailsWindow';

type ProductDetailsProps = {
	product: Product;
};

const ProductDetails: FC<ProductDetailsProps> = ({ product }) => {
	const details = [
		{ field: 'Quantity', value: product.quantity.toString() },
		{ field: 'Price', value: product.price.toPrecision(3) },
		{ field: 'Category', value: 'Some category' },
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
