import React, { FC } from 'react';

import { Divider, Grid, Typography } from '@material-ui/core';
import CheckCircleOutlinedIcon from '@material-ui/icons/CheckCircleOutlined';
import RemoveCircleOutlineIcon from '@material-ui/icons/RemoveCircleOutline';

import { Appointee, Permission } from '../../types';
import DetailsWindow from './DetailsWindow';

type AppointeeDetailsProps = {
	appointee: Appointee;
};

const permissions: Permission[] = [
	'manage products',
	'get appointments',
	'appoint manager',
	'remove manager',
	'get history',
	'manage purchase policy',
	'manage discount policy',
];

function permissionToString(permission: Permission) {
	const map: { [key in Permission]: string } = {
		'appoint manager': 'Appoint managers',
		'get appointments': 'Get appointments',
		'get history': 'Get purchase history',
		'manage products': 'Manager products',
		'remove manager': 'Remove managers',
		'manage purchase policy': 'Manager purchase policy',
		'manage discount policy': 'Manager discount policy',
	};
	return map[permission];
}

const AppointeeDetails: FC<AppointeeDetailsProps> = ({ appointee }) => {
	const details = [{ field: 'Role', value: appointee.role }];
	return (
		<DetailsWindow header={`${appointee.username}`} details={details}>
			{appointee.permissions && (
				<>
					<Typography>Permissions:</Typography>
					<Divider className="permissions-divider" />
					<Grid container spacing={1}>
						{permissions.map((permission) => (
							<>
								<Grid item xs={5} key={permission}>
									<Typography>{permissionToString(permission)}:</Typography>
								</Grid>
								<Grid item xs={7} key={permission + ' is permitted'}>
									{appointee.permissions.includes(permission) ? (
										<CheckCircleOutlinedIcon />
									) : (
										<RemoveCircleOutlineIcon />
									)}
								</Grid>
							</>
						))}
					</Grid>
				</>
			)}
		</DetailsWindow>
	);
};

export default AppointeeDetails;
