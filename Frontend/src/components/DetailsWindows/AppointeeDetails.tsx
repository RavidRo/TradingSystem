import React, { FC } from 'react';

import { Appointee } from '../../types';
import DetailsWindow from './DetailsWindow';
import PermissionsList from '../PermissionsList';

type AppointeeDetailsProps = {
	appointee: Appointee;
};

const AppointeeDetails: FC<AppointeeDetailsProps> = ({ appointee }) => {
	const details = [{ field: 'Role', value: appointee.role }];
	return (
		<DetailsWindow header={`${appointee.username}`} details={details}>
			<PermissionsList permissions={appointee.permissions} />
		</DetailsWindow>
	);
};

export default AppointeeDetails;
