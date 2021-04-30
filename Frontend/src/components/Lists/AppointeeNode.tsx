import {
	List,
	ListItem,
	ListItemText,
	Collapse,
	ListItemSecondaryAction,
	IconButton,
} from '@material-ui/core';
import { ExpandLess, ExpandMore } from '@material-ui/icons';
import React, { FC } from 'react';
import { Appointee } from '../../types';
// import '../styles/AppointeeTree.scss';

type AppointeeNodeProps = {
	appointee: Appointee;
	isSelected: (appointee: Appointee) => boolean;
	onClick: (appointee: Appointee) => void;
};

const AppointeeNode: FC<AppointeeNodeProps> = ({ appointee, isSelected, onClick }) => {
	const [open, setOpen] = React.useState(true);

	const handleClick = () => {
		setOpen(!open);
	};

	return (
		<>
			<ListItem button selected={isSelected(appointee)} onClick={() => onClick(appointee)}>
				<ListItemText
					primary={`${appointee.name} - ${appointee.role}`}
					// className="first-field"
				/>
				{appointee.children.length > 0 && (
					<ListItemSecondaryAction onClick={handleClick}>
						<IconButton edge="start" aria-label="delete">
							{open ? <ExpandLess /> : <ExpandMore />}
						</IconButton>
					</ListItemSecondaryAction>
				)}
			</ListItem>
			<Collapse in={open} timeout="auto">
				<List component="div" disablePadding style={{ paddingLeft: '20px' }}>
					{appointee.children.map((appointee) => (
						<AppointeeNode
							key={appointee.id}
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
