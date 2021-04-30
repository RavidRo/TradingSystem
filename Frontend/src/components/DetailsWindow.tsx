import { Divider, Grid, Typography } from '@material-ui/core';
import React, { FC } from 'react';

type GridItemProps = { field: string; value: string };

const GridItem: FC<GridItemProps> = ({ field, value }) => (
	<>
		<Grid item xs={2}>
			<Typography>{field}:</Typography>
		</Grid>
		<Grid item xs={10}>
			<Typography>{value}</Typography>
		</Grid>
	</>
);
type DetailsWindowProps = {
	header: string;
	details: GridItemProps[];
};

const DetailsWindow: FC<DetailsWindowProps> = ({ header, details }) => {
	return (
		<div className="details-window">
			<p className="header">{header}</p>
			<Divider className="divider" />
			<div className="grid">
				<Grid container spacing={3}>
					{/* <GridItem field="Quantity:" value={product.quantity.toString()} />
				<GridItem field="Price:" value={product.price.toPrecision(3)} />
				<GridItem field="Category:" value="Some category" /> */}
					{details.map((detail, index) => (
						<GridItem key={index} {...detail} />
					))}
				</Grid>
			</div>
		</div>
	);
};

export default DetailsWindow;
