import React, { FC } from 'react';

import { List, ListItem, ListItemText, Collapse, ListItemSecondaryAction } from '@material-ui/core';
import { ExpandLess, ExpandMore } from '@material-ui/icons';
import DeleteForeverOutlinedIcon from '@material-ui/icons/DeleteForeverOutlined';
import EditIcon from '@material-ui/icons/Edit';

import { Appointee } from '../../types';
import SecondaryActionButton from './SecondaryActionButton';
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
						<SecondaryActionButton onClick={() => onEdit(appointee)}>
							<EditIcon />
						</SecondaryActionButton>
					)}
					{onDelete && (
						<SecondaryActionButton onClick={() => onDelete(appointee.username)}>
							<DeleteForeverOutlinedIcon />
						</SecondaryActionButton>
					)}
					{appointee.appointees.length > 0 && (
						<SecondaryActionButton onClick={handleClick}>
							{open ? <ExpandLess /> : <ExpandMore />}
						</SecondaryActionButton>
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
