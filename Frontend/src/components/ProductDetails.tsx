import { Divider, Grid, Typography } from '@material-ui/core';
import React, { FC } from 'react';
import { Product } from '../types';

const GridItem: FC<{ field: string; value: string }> = ({ field, value }) => (
	<>
		<Grid item xs={2}>
			<Typography>{field}</Typography>
		</Grid>
		<Grid item xs={10}>
			<Typography>{value}</Typography>
		</Grid>
	</>
);
type ProductDetailsProps = {
	product: Product;
};

const ProductDetails: FC<ProductDetailsProps> = ({ product }) => {
	return (
		<div className="product-details">
			<h4>
				{product.name} - {product.id}
			</h4>
			<Divider className="divider" />
			<Grid container spacing={3}>
				<GridItem field="Quantity:" value={product.quantity.toString()} />
				<GridItem field="Price:" value={product.price.toPrecision(3)} />
				<GridItem field="Category:" value="Some category" />
			</Grid>
		</div>
	);
};

export default ProductDetails;
