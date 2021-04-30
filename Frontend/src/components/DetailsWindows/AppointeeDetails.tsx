import React, { FC } from 'react';

import { Divider, Grid, Typography } from '@material-ui/core';
import CheckCircleOutlinedIcon from '@material-ui/icons/CheckCircleOutlined';
import RemoveCircleOutlineIcon from '@material-ui/icons/RemoveCircleOutline';

import { Appointee, Permission } from '../../types';
import DetailsWindow from './DetailsWindow';

type AppointeeDetailsProps = {
	appointee: Appointee;
};

function permissionToString(permission: Permission) {
	const map: { [key in Permission]: string } = {
		appoint_manager: 'Appoint managers',
		get_appointments: 'Get appointments',
		get_history: 'Get purchase history',
		manage_products: 'Manager products',
		remove_manager: 'Remove managers',
	};
	return map[permission];
}

const AppointeeDetails: FC<AppointeeDetailsProps> = ({ appointee }) => {
	const details = [{ field: 'Role', value: appointee.role }];
	return (
		<DetailsWindow header={`${appointee.name} - ${appointee.id}`} details={details}>
			{appointee.permissions && (
				<>
					<Typography>Permissions:</Typography>
					<Divider className="permissions-divider" />
					<Grid container spacing={1}>
						{Object.entries(appointee.permissions).map(
							([permission_name, permitted]) => (
								<>
									<Grid item xs={5}>
										<Typography>
											{permissionToString(permission_name as Permission)}:
										</Typography>
									</Grid>
									<Grid item xs={7}>
										{permitted ? (
											<CheckCircleOutlinedIcon />
										) : (
											<RemoveCircleOutlineIcon />
										)}
									</Grid>
								</>
							)
						)}
					</Grid>
				</>
			)}
		</DetailsWindow>
	);
};

export default AppointeeDetails;
