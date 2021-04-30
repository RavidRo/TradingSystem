import { Divider, List, ListItem, ListItemText, Typography } from '@material-ui/core';
import React, { FC } from 'react';
// import '../styles/GenericList.scss';

type GenericListProps = {
	data: any[];
	header?: string;
	children: (data: any, index: number) => JSX.Element;
	createTxt?: string;
	onCreate?: () => void;
	narrow?: boolean;
	padRight?: boolean;
};

const GenericList: FC<GenericListProps> = ({
	data,
	header,
	narrow = false,
	children,
	onCreate,
	createTxt,
	padRight = false,
}) => {
	return (
		<List component="div">
			{header && (
				<>
					<ListItem>
						<Typography>{header}</Typography>
					</ListItem>
					<Divider />
				</>
			)}
			<div className={narrow ? 'narrow-list' : '' + (padRight ? 'list-padding' : '')}>
				{data.map((current, index) => children(current, index))}
				{onCreate && (
					<ListItem button onClick={onCreate}>
						<ListItemText primary={createTxt} />
					</ListItem>
				)}
			</div>
		</List>
	);
};

export default GenericList;
