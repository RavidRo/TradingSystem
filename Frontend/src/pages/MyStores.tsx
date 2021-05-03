import React, { FC, useEffect, useState } from 'react';

import { ListItem } from '@material-ui/core';
import ListItemText from '@material-ui/core/ListItemText';

import '../styles/MyStores.scss';
import { allPermissions, Appointee, defaultPermissions } from '../types';
import CreateStoreForm from '../components/FormWindows/CreateStoreForm';
import ManageStore from '../components/ManageStore';
import GenericList from '../components/Lists/GenericList';
import useAPI from '../hooks/useAPI';

// const init_stores: Store[] = [
// 	{ id: '0', name: 'Tiffany&Stuff', ids_to_quantities: {} },
// 	{ id: '1', name: 'Fluffy My Puppy', ids_to_quantities: {} },
// ];

// const products_per_store: { [key: string]: Product[] } = {
// 	'0': [
// 		{
// 			id: '0',
// 			name: 'Milk',
// 			price: 20,
// 			keywords: [],
// 			category: 'Food',
// 		},
// 		{
// 			id: '1',
// 			name: 'Bamba',
// 			price: 3.2,
// 			keywords: ['Food', 'Yummy'],
// 			category: 'Snacks',
// 		},
// 		{
// 			id: '2',
// 			name: 'Tomato',
// 			price: 2.34,
// 			keywords: ['Vegetable', 'Red'],
// 			category: 'Vegetables',
// 		},
// 	],
// 	'1': [
// 		{
// 			id: '0',
// 			name: 'Red paint',
// 			price: 20,
// 			keywords: ['Paint', 'Epic'],
// 			category: 'Construction',
// 		},
// 	],
// };

type MyStoresProps = {
	username: string;
};

type MyStore = { id: string; name: string; role: string; appointment: Appointee };

const MyStores: FC<MyStoresProps> = ({ username }) => {
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

	const onSelectStore = (storeId: string, appointment: Appointee) => {
		if (storeId !== selectedStore) {
			setSelectedStore(storeId);
			setTabAnimation(() => <ManageStore storeId={storeId} appointment={appointment} />);
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
							isManager: false,
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
							onClick={() => onSelectStore(store.id, store.appointment)}
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
