import React, { FC, useEffect, useState } from 'react';

import useAPI from '../../hooks/useAPI';
import { Appointee } from '../../types';
import AppointeeNode from './AppointeeNode';
import GenericList from './GenericList';

type AppointeesListProps = {
	selectedItem: string;
	storeId: string;
	onSelectAppointee: (appointee: Appointee) => void;
};

const AppointeesList: FC<AppointeesListProps> = ({ selectedItem, storeId, onSelectAppointee }) => {
	const { request } = useAPI<Appointee>('/get_store_appointments', {
		store_id: storeId,
	});
	const [appointees, setAppointees] = useState<Appointee[]>([]);

	useEffect(() => {
		request().then(({ data, error }) => {
			if (!error && data !== null) {
				setAppointees([data.data]);
			}
		});
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, []);
	return (
		<GenericList data={appointees} header="Store's appointments" narrow>
			{(appointee) => (
				<AppointeeNode
					key={appointee.username}
					appointee={appointee}
					isSelected={(appointee) => selectedItem === appointee.username}
					onClick={(appointee) => onSelectAppointee(appointee)}
				/>
			)}
		</GenericList>
	);
};

export default AppointeesList;
