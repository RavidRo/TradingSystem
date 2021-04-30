import React, { FC } from 'react';
import { Appointee } from '../types';
import AppointeeList from './AppointeeList';
// import '../styles/AppointeeTree.scss';

type AppointeeNodeProps = {
	appointees: Appointee[];
};

const AppointeeNode: FC<AppointeeNodeProps> = ({ appointees }) => {
	return (
		<>
			{appointees.map((appointee) => (
				<AppointeeList appointee={appointee} />
			))}
		</>
	);
};

export default AppointeeNode;
