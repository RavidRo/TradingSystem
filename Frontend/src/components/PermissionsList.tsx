import React, { FC } from 'react';

import { Checkbox, Divider, Grid, Typography } from '@material-ui/core';
import CheckCircleOutlinedIcon from '@material-ui/icons/CheckCircleOutlined';
import RemoveCircleOutlineIcon from '@material-ui/icons/RemoveCircleOutline';

import { allPermissions, Permission, permissionToString } from '../types';

type PermissionsListProps = {
	permissions: Permission[];
	setPermissions?: (permissions: Permission[]) => void;
};

const PermissionsList: FC<PermissionsListProps> = ({ permissions, setPermissions }) => {
	const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
		if (setPermissions) {
			if (event.target.checked) {
				setPermissions([...permissions, event.target.name as Permission]);
			} else {
				setPermissions(
					permissions.filter((permission) => permission !== event.target.name)
				);
			}
		}
	};

	return (
		<>
			<Typography>Permissions:</Typography>
			<Divider className="permissions-divider" />
			<Grid container spacing={1}>
				{allPermissions.map((permission) => (
					<>
						<Grid item xs={5} key={permission}>
							<Typography>{permissionToString(permission)}:</Typography>
						</Grid>
						<Grid item xs={7} key={permission + ' is permitted'}>
							{!setPermissions ? (
								permissions.includes(permission) ? (
									<CheckCircleOutlinedIcon />
								) : (
									<RemoveCircleOutlineIcon />
								)
							) : (
								<Checkbox
									checked={permissions.includes(permission)}
									onChange={handleChange}
									name={permission}
								/>
							)}
						</Grid>
					</>
				))}
			</Grid>{' '}
		</>
	);
};

export default PermissionsList;
