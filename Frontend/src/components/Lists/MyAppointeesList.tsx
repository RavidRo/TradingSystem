import React, { FC, useEffect, useState } from 'react';
import useAPI from '../../hooks/useAPI';
import { Appointee, defaultPermissions, Role } from '../../types';
import CreateAppointeeForm from '../FormWindows/CreateAppointeeForm';
// import '../styles/AppointeesList.scss';
import AppointeeNode from './AppointeeNode';
import GenericList from './GenericList';

type MyAppointeesListProps = {
	openTab: (component: FC, selectedItem: string) => void;
	selectedItem: string;
	storeId: string;
	onSelectAppointee: (appointee: Appointee) => void;
	store_name: string;
};

const MyAppointeesList: FC<MyAppointeesListProps> = ({
	openTab,
	selectedItem,
	storeId,
	onSelectAppointee,
	store_name,
}) => {
	const getMyAppointees = useAPI<Appointee[]>('/get_my_appointees', {
		store_id: storeId,
	});
	const appointManager = useAPI<{ cookie: string; answer: boolean }>(
		'/appoint_manager',
		{
			store_id: storeId,
		},
		'POST'
	);
	const appointOwner = useAPI<{ cookie: string; answer: boolean }>(
		'/appoint_manager',
		{
			store_id: storeId,
		},
		'POST'
	);
	const [myAppointees, setMyAppointees] = useState<Appointee[]>([]);

	useEffect(() => {
		getMyAppointees.request().then((getMyAppointees) => {
			if (!getMyAppointees.error && getMyAppointees.data !== null) {
				setMyAppointees(getMyAppointees.data);
			}
		});
	}, []);

	const onAppoint = (username: string, role: Role) => {
		const request = role === 'Manager' ? appointManager : appointOwner;
		request.request().then((request) => {
			if (!request.error && request.data !== null && request.data.answer) {
				setMyAppointees([
					{
						appointees: [],
						isManager: role === 'Manager',
						role,
						store_id: storeId,
						username,
						store_name: store_name,
						permissions: defaultPermissions,
					},
					...myAppointees,
				]);
			}
		});
	};

	const openAppointeeForm = () => {
		openTab(() => <CreateAppointeeForm onSubmit={onAppoint} />, '');
	};

	return (
		<GenericList
			data={myAppointees}
			onCreate={openAppointeeForm}
			header="My appointees"
			createTxt="+ Appoint a new member"
			narrow
		>
			{(appointee) => (
				<AppointeeNode
					key={appointee.id}
					appointee={appointee}
					isSelected={(appointee) => selectedItem === appointee.username}
					onClick={(appointee) => onSelectAppointee(appointee)}
					onDelete={() => {}}
				/>
			)}
		</GenericList>
	);
};

export default MyAppointeesList;
