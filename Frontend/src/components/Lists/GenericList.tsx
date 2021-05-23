import { Divider, List, ListItem, ListItemText, Typography } from '@material-ui/core';
import React, { FC } from 'react';

type GenericListProps = {
	data: any[];
	header?: string;
	children: (data: any, index: number) => JSX.Element;
	createTxt?: string;
	onCreate?: () => void;
	narrow?: boolean;
	padRight?: boolean;
	onDrop?: (event: React.DragEvent) => void;
};

const GenericList: FC<GenericListProps> = ({
	data,
	header,
	narrow = false,
	children,
	onCreate,
	createTxt,
	padRight = false,
	onDrop,
}) => {
	const onDragOver = (event: React.DragEvent) => {
		if (onDrop) {
			event.preventDefault();
		}
	};

	return (
		<List component="div">
			{header && (
				<>
					<div onDrop={onDrop} onDragOver={onDragOver}>
						<ListItem>
							<Typography>{header}</Typography>
						</ListItem>
					</div>
					<Divider />
				</>
			)}
			<div className={narrow ? 'narrow-list' : '' + (padRight ? 'list-padding' : '')}>
				{data.map((current, index) => children(current, index))}
				{onCreate && (
					<ListItem key={'random_key'} button onClick={onCreate}>
						<ListItemText primary={createTxt} />
					</ListItem>
				)}
			</div>
		</List>
	);
};

export default GenericList;
