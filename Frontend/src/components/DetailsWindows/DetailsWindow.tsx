import React, { FC } from 'react';

import { Divider, Grid, List, ListItem, Typography } from '@material-ui/core';

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

const DetailsWindow: FC<DetailsWindowProps> = ({ header, details, children }) => {
	return (
		<div className="details-window">
			<List>
				<ListItem>
					<Typography>{header}</Typography>
				</ListItem>
				<Divider className="divider" />
				<div className="details">
					<div className="grid">
						<Grid container spacing={3}>
							{details.map((detail, index) => (
								<GridItem key={index} {...detail} />
							))}
						</Grid>
					</div>
					{children}
				</div>
			</List>
		</div>
	);
};

export default DetailsWindow;
