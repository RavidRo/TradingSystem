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
import EditIcon from '@material-ui/icons/Edit';

import { Appointee } from '../../types';
// import '../styles/AppointeeTree.scss';

type AppointeeNodeProps = {
	appointee: Appointee;
	isSelected: (appointee: Appointee) => boolean;
	onClick: (appointee: Appointee) => void;
	onDelete?: (appointeeUsername: string) => void;
	onEdit?: (appointee: Appointee) => void;
};

const AppointeeNode: FC<AppointeeNodeProps> = ({
	appointee,
	isSelected,
	onClick,
	onDelete,
	onEdit,
}) => {
	const [open, setOpen] = React.useState(true);

	const handleClick = () => {
		setOpen(!open);
	};

	return (
		<>
			<ListItem button selected={isSelected(appointee)} onClick={() => onClick(appointee)}>
				<ListItemText key="details" primary={`${appointee.username} - ${appointee.role}`} />

				<ListItemSecondaryAction key="expandAndDelete">
					{onEdit && appointee.is_manager && (
						<span className="secondary-second-action">
							<IconButton
								edge="end"
								aria-label="delete"
								onClick={() => onEdit(appointee)}
							>
								<EditIcon />
							</IconButton>
						</span>
					)}
					{onDelete && (
						<span className="secondary-second-action">
							<IconButton
								edge="end"
								aria-label="delete"
								onClick={() => onDelete(appointee.username)}
							>
								<DeleteForeverOutlinedIcon />
							</IconButton>
						</span>
					)}
					{appointee.appointees.length > 0 && (
						<IconButton edge="start" aria-label="expand" onClick={handleClick}>
							{open ? <ExpandLess /> : <ExpandMore />}
						</IconButton>
					)}
				</ListItemSecondaryAction>
			</ListItem>

			<Collapse in={open} timeout="auto">
				<List component="div" disablePadding style={{ paddingLeft: '20px' }}>
					{appointee.appointees.map((appointee) => (
						<AppointeeNode
							key={appointee.username}
							appointee={appointee}
							isSelected={isSelected}
							onClick={onClick}
							onEdit={onEdit}
						/>
					))}
				</List>
			</Collapse>
		</>
	);
};

export default AppointeeNode;
