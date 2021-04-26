import React, { FC, useState } from 'react';

import { ListItem } from '@material-ui/core';
import ListItemText from '@material-ui/core/ListItemText';

import '../styles/MyStores.scss';
import { Store, Product } from '../types';
import CreateStoreForm from '../components/CreateStoreForm';
import ManageStore from '../components/ManageStore';
import GenericList from '../components/GenericList';

const init_stores: Store[] = [
	{ id: '0', name: 'Tiffany&Stuff', role: 'Founder' },
	{ id: '1', name: 'Fluffy My Puppy', role: 'Member' },
];

const products_per_store: { [key: string]: Product[] } = {
	'0': [
		{
			id: '0',
			name: 'Milk',
			price: 20,
			quantity: 2,
		},
		{
			id: '1',
			name: 'Bamba',
			price: 3.2,
			quantity: 2,
		},
		{
			id: '2',
			name: 'Tomato',
			price: 2.34,
			quantity: 5,
		},
	],
	'1': [
		{
			id: '0',
			name: 'Red paint',
			price: 20,
			quantity: 2,
		},
	],
};

type MyStoresProps = {};

const MyStores: FC<MyStoresProps> = () => {
	const [selectedStore, setSelectedStore] = useState<string | null>(null);
	const [stores, setStores] = useState<Store[]>(init_stores);
	const [open, setOpen] = useState(false);

	const setStore = (storeId: string) => {
		setTab(storeId);
	};

	const openStoreForm = () => {
		setTab(null);
	};
	const setTab = (selectedStore: string | null) => {
		setOpen(false);
		setTimeout(() => {
			setSelectedStore(selectedStore);
			setOpen(true);
		}, 300);
	};

	const onNewStore = (newName: string) => {
		const store: Store = { id: '4', name: newName, role: 'Founder' };
		setStores(stores.concat([store]));
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
					{(store) => (
						<ListItem
							key={store.id}
							button
							onClick={() => setStore(store.id)}
							selected={store.id === selectedStore}
						>
							<ListItemText primary={`${store.name} - ${store.role}`} />
						</ListItem>
					)}
				</GenericList>
			</div>
			<div className={'second-tab' + (open ? ' open' : '')}>
				{selectedStore ? (
					<ManageStore products={products_per_store[selectedStore] || []} />
				) : (
					<CreateStoreForm onSubmit={onNewStore} />
				)}
			</div>
		</div>
	);
};

export default MyStores;
