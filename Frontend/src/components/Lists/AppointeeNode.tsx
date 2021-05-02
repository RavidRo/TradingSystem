import React, { FC } from 'react';

import {
	List,
	ListItem,
	ListItemText,
	Collapse,
	ListItemSecondaryAction,
	IconButton,
} from '@material-ui/core';
import { ExpandLess, ExpandMore } from '@material-ui/icons';
import DeleteForeverOutlinedIcon from '@material-ui/icons/DeleteForeverOutlined';

import { Appointee } from '../../types';
// import '../styles/AppointeeTree.scss';

type AppointeeNodeProps = {
	appointee: Appointee;
	isSelected: (appointee: Appointee) => boolean;
	onClick: (appointee: Appointee) => void;
	onDelete?: (appointeeUsername: string) => void;
};

const AppointeeNode: FC<AppointeeNodeProps> = ({ appointee, isSelected, onClick, onDelete }) => {
	const [open, setOpen] = React.useState(true);

	const handleClick = () => {
		setOpen(!open);
	};

	return (
		<>
			<ListItem button selected={isSelected(appointee)} onClick={() => onClick(appointee)}>
				<ListItemText
					key="details"
					primary={`${appointee.username} - ${appointee.role}`}
					// className="first-field"
				/>
				{onDelete && (
					<ListItemSecondaryAction
						key="delete"
						onClick={() => onDelete(appointee.username)}
					>
						<IconButton edge="end" aria-label="delete">
							<DeleteForeverOutlinedIcon />
						</IconButton>
					</ListItemSecondaryAction>
				)}
				{appointee.appointees.length > 0 && (
					<ListItemSecondaryAction key="expand" onClick={handleClick}>
						<IconButton edge="start" aria-label="expand">
							{open ? <ExpandLess /> : <ExpandMore />}
						</IconButton>
					</ListItemSecondaryAction>
				)}
			</ListItem>

			<Collapse in={open} timeout="auto">
				<List component="div" disablePadding style={{ paddingLeft: '20px' }}>
					{appointee.appointees.map((appointee) => (
						<AppointeeNode
							key={appointee.username}
							appointee={appointee}
							isSelected={isSelected}
							onClick={onClick}
						/>
					))}
				</List>
			</Collapse>
		</>
	);
};

export default AppointeeNode;
