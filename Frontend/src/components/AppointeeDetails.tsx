import React, { FC } from 'react';
import { Appointee } from '../types';
import DetailsWindow from './DetailsWindow';

type AppointeeDetailsProps = {
	appointee: Appointee;
};

const AppointeeDetails: FC<AppointeeDetailsProps> = ({ appointee }) => {
	const details = [{ field: 'Role', value: appointee.role }];
	return <DetailsWindow header={`${appointee.name} - ${appointee.id}`} details={details} />;
};

export default AppointeeDetails;
