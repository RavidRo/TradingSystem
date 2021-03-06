import React, { FC, useContext, useEffect, useState } from 'react';

import { ListItem } from '@material-ui/core';
import ListItemText from '@material-ui/core/ListItemText';

import '../styles/MyStoresPage/MyStores.scss';
import { allPermissions, Appointee } from '../types';
import CreateStoreForm from '../components/FormWindows/CreateForms/CreateStoreForm';
import ManageStore from '../components/ManageStore';
import GenericList from '../components/Lists/GenericList';
import useAPI from '../hooks/useAPI';
import { UsernameContext } from '../contexts';

type MyStoresProps = {};

type MyStore = { id: string; name: string; role: string; appointment: Appointee };

const MyStores: FC<MyStoresProps> = () => {
	const username = useContext(UsernameContext);
	const myResponsibilities = useAPI<Appointee[]>('/get_my_appointments');
	const openStore = useAPI<string>('/create_store', {}, 'POST');
	useEffect(() => {
		myResponsibilities.request({}, (data, error) => {
			if (!error && data !== null) {
				const myStores = data.data.map((responsibility) => ({
					id: responsibility.store_id,
					name: responsibility.store_name,
					role: responsibility.role,
					appointment: responsibility,
				}));
				setStores(myStores);
			}
		});
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, []);

	const [stores, setStores] = useState<MyStore[]>([]);
	const [selectedStore, setSelectedStore] = useState<string>('');
	const [open, setOpen] = useState<boolean>(false);
	const [Tab, setTab] = useState<FC | null>(null);

	const setAppointment = (storeId: string, appointment: Appointee) => {
		setStores((myStores) =>
			myStores.map((store) => (store.id !== storeId ? store : { ...store, appointment }))
		);
	};

	const onSelectStore = (storeToOpen: MyStore) => {
		if (storeToOpen.id !== selectedStore && storeToOpen) {
			setSelectedStore(storeToOpen.id);
			setTabAnimation(() => (
				<ManageStore
					storeId={storeToOpen.id}
					appointment={storeToOpen.appointment}
					setAppointment={setAppointment}
				/>
			));
		}
	};

	const openStoreForm = () => {
		setSelectedStore('');
		setTabAnimation(() => <CreateStoreForm onSubmit={onNewStore} />);
	};
	const setTabAnimation = (components: FC) => {
		setOpen(false);
		setTimeout(() => {
			setTab(() => components);
			setOpen(true);
		}, 300);
	};

	const onNewStore = (newName: string) => {
		openStore.request({ name: newName }, (data, error) => {
			if (!error && data !== null) {
				setStores([
					{
						id: data.data,
						name: newName,
						role: 'Founder',
						appointment: {
							appointees: [],
							is_manager: false,
							permissions: allPermissions,
							role: 'Founder',
							store_id: data.data,
							store_name: newName,
							username: username,
						},
					},
					...stores,
				]);
			}
		});
	};

	return (
		<div className="my-stores-page">
			<div className="stores-list">
				<GenericList
					data={stores}
					onCreate={openStoreForm}
					header="My Stores"
					createTxt="+ Create a new store"
				>
					{(store: MyStore) => (
						<ListItem
							key={store.id}
							button
							onClick={() => onSelectStore(store)}
							selected={store.id === selectedStore}
						>
							<ListItemText primary={`${store.name} - ${store.role}`} />
						</ListItem>
					)}
				</GenericList>
			</div>
			<div className={'second-tab' + (open ? ' open' : '')}>{Tab && <Tab />}</div>
		</div>
	);
};

export default MyStores;
