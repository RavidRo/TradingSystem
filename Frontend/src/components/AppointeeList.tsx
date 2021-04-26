import { List, ListItem, ListItemText, Collapse } from '@material-ui/core';
import { ExpandLess, ExpandMore } from '@material-ui/icons';
import React, { FC } from 'react';
import { Appointee } from '../types';
import AppointeeNode from './AppointeeNode';
// import '../styles/AppointeeTree.scss';

type AppointeeListProps = {
	appointee: Appointee;
};

const AppointeeList: FC<AppointeeListProps> = ({ appointee }) => {
	const [open, setOpen] = React.useState(true);

	const handleClick = () => {
		setOpen(!open);
	};

	return (
		<>
			<ListItem key={appointee.id} button onClick={handleClick}>
				<ListItemText primary={appointee.name} />
				{open ? <ExpandLess /> : <ExpandMore />}
			</ListItem>
			<Collapse key={appointee.id} in={open} timeout="auto">
				<List component="div" disablePadding style={{ paddingLeft: '20px' }}>
					<AppointeeNode appointees={appointee.children} />
				</List>
			</Collapse>
		</>
	);
};

export default AppointeeList;
