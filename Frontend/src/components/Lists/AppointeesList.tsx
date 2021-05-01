import React, { FC, useEffect, useState } from 'react';

import useAPI from '../../hooks/useAPI';
import { Appointee } from '../../types';
import AppointeeNode from './AppointeeNode';
import GenericList from './GenericList';

type AppointeesListProps = {
	selectedItem: string;
	store_id: string;
	onSelectAppointee: (appointee: Appointee) => void;
};

const AppointeesList: FC<AppointeesListProps> = ({ selectedItem, store_id, onSelectAppointee }) => {
	const { request, data, error } = useAPI<Appointee[]>('/get_store_appointments', {
		store_id: store_id,
	});
	const [appointees, setAppointees] = useState<Appointee[]>([]);

	useEffect(() => {
		request().then(() => {
			if (!error && data !== null) {
				setAppointees(data);
			}
		});
	}, []);
	return (
		<GenericList data={appointees} header="Store's appointments" narrow>
			{(appointee) => (
				<AppointeeNode
					appointee={appointee}
					isSelected={(appointee) => selectedItem === appointee.username}
					onClick={(appointee) => onSelectAppointee(appointee)}
				/>
			)}
		</GenericList>
	);
};

export default AppointeesList;
