import React, { FC, useState } from 'react';

import { ListItem } from '@material-ui/core';
import ListItemText from '@material-ui/core/ListItemText';

import '../styles/MyStores.scss';
import { Store, Product } from '../types';
import CreateStoreForm from '../components/FormWindows/CreateStoreForm';
import ManageStore from '../components/ManageStore';
import GenericList from '../components/Lists/GenericList';

const init_stores: Store[] = [
	{ id: '0', name: 'Tiffany&Stuff', role: 'Founder' },
	{ id: '1', name: 'Fluffy My Puppy', role: 'Owner' },
];

const products_per_store: { [key: string]: Product[] } = {
	'0': [
		{
			id: '0',
			name: 'Milk',
			price: 20,
			quantity: 2,
			keywords: [],
			category: 'Food',
		},
		{
			id: '1',
			name: 'Bamba',
			price: 3.2,
			quantity: 2,
			keywords: ['Food', 'Yummy'],
			category: 'Snacks',
		},
		{
			id: '2',
			name: 'Tomato',
			price: 2.34,
			quantity: 5,
			keywords: ['Vegetable', 'Red'],
			category: 'Vegetables',
		},
	],
	'1': [
		{
			id: '0',
			name: 'Red paint',
			price: 20,
			quantity: 2,
			keywords: ['Paint', 'Epic'],
			category: 'Construction',
		},
	],
};

type MyStoresProps = {};

const MyStores: FC<MyStoresProps> = () => {
	const [stores, setStores] = useState<Store[]>(init_stores);
	const [selectedStore, setSelectedStore] = useState<string>('');
	const [open, setOpen] = useState<boolean>(false);
	const [Tab, setTab] = useState<FC | null>(null);

	const onSelectStore = (store: Store) => {
		if (store.id !== selectedStore) {
			setSelectedStore(store.id);
			setTabAnimation(() => <ManageStore products={products_per_store[store.id] || []} />);
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
