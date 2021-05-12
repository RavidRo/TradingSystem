import React, { FC, useState } from 'react';

import useAPI from '../../hooks/useAPI';
import { allPermissions, Appointee, defaultPermissions, Permission, Role } from '../../types';
import CreateAppointeeForm from '../FormWindows/CreateForms/CreateAppointeeForm';
import EditPermissionsForm from '../FormWindows/EditForms/EditPermissionsForm';
import AppointeeNode from './AppointeeNode';
import GenericList from './GenericList';

type MyAppointeesListProps = {
	openTab: (component: FC, selectedItem: string) => void;
	selectedItem: string;
	storeId: string;
	onSelectAppointee: (appointee: Appointee) => void;
	store_name: string;
	appointment: Appointee;
	setAppointment: (storeId: string, appointment: Appointee) => void;
};

const MyAppointeesList: FC<MyAppointeesListProps> = ({
	openTab,
	selectedItem,
	storeId,
	onSelectAppointee,
	store_name,
	appointment,
	setAppointment,
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
	const setAppointees = (newAppointees: Appointee[]) => {
		setAppointment(storeId, {
			...appointment,
			appointees: newAppointees,
		});
		setMyAppointees(newAppointees);
	};
	const onAppoint = (username: string, role: Role) => {
		const request = role === 'Manager' ? appointManager : appointOwner;
		request.request({ username: username }).then((request) => {
			if (!request.error && request.data !== null && request.data.succeeded) {
				setAppointees([
					{
						appointees: [],
						is_manager: role === 'Manager',
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
				setAppointees(
					appointment.appointees.filter(
						(myAppointee) => myAppointee.username !== appointeeUsername
					)
				);
			}
		});
	};
	const addPermission = useAPI('/add_manager_permission', { store_id: storeId }, 'POST');
	const removePermission = useAPI('/remove_manager_permission', { store_id: storeId }, 'POST');
	const onEditAppointeeForm = (appointee: Appointee) => {
		const onEdit = (newPermissions: Permission[]) => {
			const promises: Promise<{ error: boolean; errorMsg: string }>[] = [];
			newPermissions.forEach((permission) => {
				if (!appointee.permissions.includes(permission)) {
					// A new permission was added (Was not in the original permissions list)
					promises.push(
						addPermission.request({ username: appointee.username, permission })
					);
				}
			});
			appointee.permissions.forEach((oldPermission) => {
				if (!newPermissions.includes(oldPermission)) {
					// An old permission in not included in the new ones(It was removed)
					removePermission.request({
						username: appointee.username,
						permission: oldPermission,
					});
				}
			});
			Promise.all(promises).then((results) => {
				if (!results.some((result) => result.error)) {
					const newAppointees = [
						...myAppointees.filter(
							(appointeeTemp) => appointeeTemp.username !== appointee.username
						),
						{ ...appointee, permissions: newPermissions },
					];
					setAppointees(newAppointees);
				}
			});
		};
		openTab(() => <EditPermissionsForm onSubmit={onEdit} appointee={appointee} />, '');
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
					onEdit={
						appointment.permissions.includes('appoint manager')
							? onEditAppointeeForm
							: undefined
					}
				/>
			)}
		</GenericList>
	);
};

export default MyAppointeesList;
