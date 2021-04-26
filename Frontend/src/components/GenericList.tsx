import { Divider, List, ListItem, ListItemText, Typography } from '@material-ui/core';
import React, { FC } from 'react';
import '../styles/GenericList.scss';

type GenericListProps = {
	data: any[];
	header: string;
	children: (data: any) => JSX.Element;
	createTxt?: string;
	onCreate?: () => void;
};

const GenericList: FC<GenericListProps> = (props) => {
	return (
		<List component="nav">
			<ListItem>
				<Typography className="header-item">{props.header}</Typography>
			</ListItem>
			<Divider />
			{props.data.map((current) => props.children(current))}
			{props.onCreate && (
				<ListItem button onClick={props.onCreate}>
					<ListItemText primary={props.createTxt} />
				</ListItem>
			)}
		</List>
	);
};

export default GenericList;
