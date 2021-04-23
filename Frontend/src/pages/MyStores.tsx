import React, { FC, useState } from 'react';

import { List, ListItem, Divider, Typography, TextField, Button } from '@material-ui/core';
import ListItemText from '@material-ui/core/ListItemText';

import '../styles/MyStores.scss';
import { Store, Product } from '../types';

const init_stores: Store[] = [
	{ id: '0', name: 'Tiffany&Stuff' },
	{ id: '1', name: 'Fluffy My Puppy' },
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

const MyStores: FC<MyStoresProps> = (props) => {
	const [stores, setStores] = useState<Store[]>(init_stores);
	const [selectedStore, setSelectedStore] = useState<string | null>(null);
	const [products, setProducts] = useState<Product[]>([]);
	const [creatingStore, setCreatingStore] = useState<boolean>(false);

	const setStore = (storeId: string) => {
		setSelectedStore(storeId);
		setProducts(products_per_store[storeId]);
	};

	const openStoreForm = () => {
		setCreatingStore(true);
		setSelectedStore(null);
		setProducts([]);
	};

	return (
		<div className="my-stores-page">
			<div className="stores-list">
				<List component="nav" aria-label="My Stores">
					<ListItem>
						<Typography className="header-item">My Stores</Typography>
					</ListItem>
					<Divider />
					{stores.map((store) => (
						<ListItem
							key={store.id}
							button
							onClick={() => setStore(store.id)}
							selected={store.id === selectedStore}
						>
							<ListItemText primary={store.name} />
						</ListItem>
					))}
					<ListItem button onClick={openStoreForm}>
						<ListItemText primary="+ Create a new store" />
					</ListItem>
				</List>
			</div>
			{selectedStore && (
				<div className="selected-store">
					<div className="products-list">
						<List component="nav" aria-label="The store's products">
							<ListItem>
								<Typography className="header-item">Products</Typography>
							</ListItem>
							<Divider />
							{products.map((product) => (
								<ListItem key={product.id} button>
									<ListItemText primary={product.name} className="product-name" />
									<ListItemText primary={`in stock: ${product.quantity}`} />
								</ListItem>
							))}
							<ListItem button>
								<ListItemText primary="+ Add a new product" />
							</ListItem>
						</List>
					</div>
					<div>
						<List component="nav" aria-label="The store's products">
							<ListItem>
								<Typography className="header-item">Appointees</Typography>
							</ListItem>
							<Divider />
							<ListItem button>
								<ListItemText primary="+ Appoint a new member" />
							</ListItem>
						</List>
					</div>
				</div>
			)}
			{creatingStore && !selectedStore && (
				<div className="create-store-form-cont">
					<h2>Creating a new store</h2>
					<form
						noValidate
						autoComplete="off"
						className="create-store-form"
						onSubmit={console.log}
					>
						<TextField
							required
							margin="normal"
							id="store-name"
							fullWidth
							label="Store's name"
						/>
						<Button type="submit" fullWidth variant="contained" color="primary">
							Create Store!
						</Button>
					</form>
				</div>
			)}
		</div>
	);
};

export default MyStores;
