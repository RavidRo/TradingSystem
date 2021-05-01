import React, { FC, useEffect, useState } from 'react';

import { Appointee, Product, Store, ProductQuantity } from '../types';
import AppointeeDetails from './DetailsWindows/AppointeeDetails';
import useAPI from '../hooks/useAPI';
import ProductsList from './Lists/ProductsList';
import MyAppointeesList from './Lists/MyAppointeesList';
import AppointeesList from './Lists/AppointeesList';
import DiscountsList from './Lists/DiscountsList';
import ConditionsList from './Lists/ConditionsList';

// const tree: Appointee[] = [
// 	{
// 		id: '11',
// 		name: 'Me',
// 		role: 'Founder',
// 		children: [
// 			{
// 				id: '12',
// 				name: 'Sean',
// 				role: 'Owner',
// 				children: [
// 					{
// 						id: '10',
// 						name: 'Tali',
// 						role: 'Owner',
// 						children: [],
// 					},
// 					{
// 						id: '14',
// 						name: 'Omer',
// 						role: 'Manager',
// 						permissions: {
// 							appoint_manager: true,
// 							get_appointments: false,
// 							get_history: false,
// 							manage_products: true,
// 							remove_manager: true,
// 						},
// 						children: [],
// 					},
// 				],
// 			},
// 			{
// 				id: '13',
// 				name: 'Inon',
// 				role: 'Manager',
// 				children: [],
// 				permissions: {
// 					appoint_manager: true,
// 					get_appointments: false,
// 					get_history: false,
// 					manage_products: true,
// 					remove_manager: true,
// 				},
// 			},
// 		],
// 	},
// ];

// const discounts: Discount[] = [
// 	{
// 		id: '26',
// 		rule: {
// 			type: {
// 				operator: 'xor',
// 				decision_rule: 'max',
// 			},
// 			operands: [
// 				{
// 					id: '27',
// 					rule: {
// 						percentage: 20,
// 						context: {
// 							obj: 'store',
// 						},
// 					},
// 				},
// 			],
// 		},
// 	},
// ];

// const conditions: Condition[] = [
// 	{
// 		id: '31',
// 		rule: {
// 			operator: 'conditioning',
// 			test: {
// 				id: '32',
// 				rule: {
// 					context: {
// 						obj: 'user',
// 					},
// 					operator: 'great-equals',
// 					target: 18,
// 				},
// 			},
// 		},
// 	},
// ];

type ManageStoreProps = {
	store: Store;
};

const ManageStore: FC<ManageStoreProps> = ({ store }) => {
	const [products, setProducts] = useState<ProductQuantity[]>([]);

	const { request: productsRequest, data: productsData, error: productsError } = useAPI<
		Product[]
	>('/get_products_by_store', {
		store_id: store.id,
	});

	useEffect(() => {
		productsRequest().then(() => {
			if (!productsError && productsData !== null) {
				setProducts(
					productsData.map((product) => ({
						...product,
						quantity: store.ids_to_quantities[product.id],
					}))
				);
			}
		});
	}, []);

	const [selectedItem, setSelectedItem] = useState<string>('');
	const [open, setOpen] = useState<boolean>(false);
	const [Tab, setTab] = useState<FC | null>(null);

	useEffect(() => {
		setOpen(false);
	}, [products]);

	const setTabAnimation = (component: FC) => {
		setOpen(false);
		setTimeout(() => {
			setTab(() => component);
			setOpen(true);
		}, 300);
	};

	const openTab = (component: FC, selectedItem: string) => {
		setSelectedItem(selectedItem);
		setTabAnimation(component);
	};

	const onSelectAppointee = (appointee: Appointee) => {
		if (appointee.username !== selectedItem) {
			openTab(() => <AppointeeDetails appointee={appointee} />, appointee.username);
		}
	};

	return (
		<div className="my-store-page">
			<div className="my-store-cont">
				<ProductsList
					openTab={openTab}
					products={products}
					selectedItem={selectedItem}
					setProducts={setProducts}
					store_id={store.id}
				/>
				<MyAppointeesList
					onSelectAppointee={onSelectAppointee}
					openTab={openTab}
					selectedItem={selectedItem}
					storeId={store.id}
					store_name={store.name}
				/>
				<AppointeesList
					onSelectAppointee={onSelectAppointee}
					selectedItem={selectedItem}
					store_id={store.id}
				/>
				<DiscountsList openTab={openTab} products={products} />
				<ConditionsList openTab={openTab} products={products} />
			</div>
			<div className={'second-tab' + (open ? ' open' : '')}>
				{Tab && (
					<div className="stick-top">
						<Tab />
					</div>
				)}
			</div>
		</div>
	);
};

export default ManageStore;
