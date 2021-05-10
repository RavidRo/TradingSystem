import React, { FC, useState } from 'react';
import useAPI from '../../hooks/useAPI';
import { allPermissions, Appointee, defaultPermissions, Role } from '../../types';
import CreateAppointeeForm from '../FormWindows/CreateForms/CreateAppointeeForm';
import AppointeeNode from './AppointeeNode';
import GenericList from './GenericList';

type MyAppointeesListProps = {
	openTab: (component: FC, selectedItem: string) => void;
	selectedItem: string;
	storeId: string;
	onSelectAppointee: (appointee: Appointee) => void;
	store_name: string;
	appointment: Appointee;
};

const MyAppointeesList: FC<MyAppointeesListProps> = ({
	openTab,
	selectedItem,
	storeId,
	onSelectAppointee,
	store_name,
	appointment,
}) => {
	const appointManager = useAPI<{ cookie: string; answer: string; succeeded: boolean }>(
		'/appoint_manager',
		{
			store_id: storeId,
		},
		'POST'
	);
	const appointOwner = useAPI<{ cookie: string; answer: string; succeeded: boolean }>(
		'/appoint_owner',
		{
			store_id: storeId,
		},
		'POST'
	);
	const removeAppointment = useAPI<{ cookie: string; answer: string; succeeded: boolean }>(
		'/remove_appointment',
		{
			store_id: storeId,
		},
		'POST'
	);
	const [myAppointees, setMyAppointees] = useState<Appointee[]>(appointment.appointees);

	const onAppoint = (username: string, role: Role) => {
		const request = role === 'Manager' ? appointManager : appointOwner;
		request.request({ username: username }).then((request) => {
			if (!request.error && request.data !== null && request.data.succeeded) {
				setMyAppointees([
					{
						appointees: [],
						isManager: role === 'Manager',
						role,
						store_id: storeId,
						username,
						store_name: store_name,
						permissions: role === 'Manager' ? defaultPermissions : allPermissions,
					},
					...myAppointees,
				]);
			}
		});
	};

	const openAppointeeForm = () => {
		openTab(() => <CreateAppointeeForm onSubmit={onAppoint} />, '');
	};

	const onDelete = (appointeeUsername: string) => {
		removeAppointment.request({ username: appointeeUsername }, (data, error) => {
			if (!error && data !== null) {
				setMyAppointees((myAppointees) =>
					myAppointees.filter((myAppointee) => myAppointee.username !== appointeeUsername)
				);
			}
		});
	};

	return (
		<GenericList
			data={myAppointees}
			onCreate={
				appointment.permissions.includes('appoint manager') ? openAppointeeForm : undefined
			}
			header="My appointees"
			createTxt="+ Appoint a new member"
			narrow
		>
			{(appointee) => (
				<AppointeeNode
					key={appointee.username}
					appointee={appointee}
					isSelected={(appointee) => selectedItem === appointee.username}
					onClick={(appointee) => onSelectAppointee(appointee)}
					onDelete={
						appointment.permissions.includes('remove manager') ? onDelete : undefined
					}
				/>
			)}
		</GenericList>
	);
};

export default MyAppointeesList;
