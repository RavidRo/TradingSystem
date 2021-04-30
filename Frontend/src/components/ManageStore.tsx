import React, { FC, useEffect, useState } from 'react';

import { ListItem, ListItemText } from '@material-ui/core';

import { Appointee, Product, Discount, Condition, Store, ProductQuantity } from '../types';
import GenericList from './Lists/GenericList';
import CreateProductForm from './FormWindows/CreateProductForm';
import ProductDetails from './DetailsWindows/ProductDetails';
import AppointeeDetails from './DetailsWindows/AppointeeDetails';
import CreateAppointeeForm from './FormWindows/CreateAppointeeForm';
import AppointeeNode from './Lists/AppointeeNode';
import DiscountNode from './Lists/DiscountNode';
import ConditionNode from './Lists/ConditionNode';
import CreateDiscountForm from './FormWindows/CreateDiscountForm';
import CreateConditionForm from './FormWindows/CreateConditionForm';
import useAPI from '../hooks/useAPI';

type ManageStoreProps = {
	store: Store;
};

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

const discounts: Discount[] = [
	{
		id: '26',
		rule: {
			type: {
				operator: 'xor',
				decision_rule: 'max',
			},
			operands: [
				{
					id: '27',
					rule: {
						percentage: 20,
						context: {
							obj: 'store',
						},
					},
				},
			],
		},
	},
];

const conditions: Condition[] = [
	{
		id: '31',
		rule: {
			operator: 'conditioning',
			test: {
				id: '32',
				rule: {
					context: {
						obj: 'user',
					},
					operator: 'great-equals',
					target: 18,
				},
			},
		},
	},
];

const ManageStore: FC<ManageStoreProps> = ({ store }) => {
	const [products, setProducts] = useState<ProductQuantity[]>([]);
	const [appointees, setAppointees] = useState<Appointee[]>([]);

	const { request: productsRequest, data: productsData, error: productsError } = useAPI<
		Product[]
	>('/get_products_by_store', {
		store_id: store.id,
	});

	const { request: appointeesRequest, data: appointeesData, error: appointeesError } = useAPI<
		Appointee[]
	>('/get_my_appointees', {
		store_id: store.id,
	});

	const createProduct = useAPI<{
		cookie: string;
		product_id: string;
	}>('/create_product', {}, 'POST');

	useEffect(() => {
		if (!productsError && productsData !== null) {
			productsRequest().then(() =>
				setProducts(
					productsData.map((product) => ({
						...product,
						quantity: store.ids_to_quantities[product.id],
					}))
				)
			);
		}
		if (!appointeesError && appointeesData !== null) {
			appointeesRequest().then(() => setAppointees(appointeesData));
		}
	}, []);

	const [selectedItem, setSelectedItem] = useState<string>('');
	const [open, setOpen] = useState<boolean>(false);

	const [Tab, setTab] = useState<FC | null>(null);

	useEffect(() => {
		setOpen(false);
	}, [products]);

	const onSelectProduct = (product: ProductQuantity) => {
		if (product.id !== selectedItem) {
			setSelectedItem(product.id);
			setTabAnimation(() => <ProductDetails product={product} />);
		}
	};

	const onSelectAppointee = (appointee: Appointee) => {
		if (appointee.username !== selectedItem) {
			setSelectedItem(appointee.username);
			setTabAnimation(() => <AppointeeDetails appointee={appointee} />);
		}
	};

	const openProductForm = () => {
		setSelectedItem('');
		setTabAnimation(() => {
			const handleSubmit = (
				name: string,
				price: number,
				quantity: number,
				category: string,
				keywords: string[]
			) => {
				createProduct
					.request({
						store_id: store.id,
						name,
						price,
						quantity,
						category,
						keywords,
					})
					.then(() => {
						if (!createProduct.error && createProduct.data !== null) {
							setProducts([
								{
									id: createProduct.data.product_id,
									name,
									price,
									category,
									keywords,
									quantity,
								},
								...products,
							]);
						}
					});
			};
			return <CreateProductForm onSubmit={handleSubmit} />;
		});
	};

	const openAppointeeForm = () => {
		setSelectedItem('');
		setTabAnimation(() => <CreateAppointeeForm onSubmit={(name) => console.log(name)} />);
	};

	const openDiscountForm = () => {
		setSelectedItem('');
		setTabAnimation(() => (
			<CreateDiscountForm onSubmit={(name) => console.log(name)} products={products} />
		));
	};

	const openConditionForm = () => {
		setSelectedItem('');
		setTabAnimation(() => (
			<CreateConditionForm onSubmit={(name) => console.log(name)} products={products} />
		));
	};

	const setTabAnimation = (components: FC) => {
		setOpen(false);
		setTimeout(() => {
			setTab(() => components);
			setOpen(true);
		}, 300);
	};

	return (
		<div className="my-store-page">
			<div className="my-store-cont">
				<GenericList
					data={products}
					onCreate={openProductForm}
					header="Products"
					createTxt="+ Add a new product"
				>
					{(product) => (
						<ListItem
							key={product.id}
							selected={selectedItem === product.id}
							onClick={() => onSelectProduct(product)}
							button
						>
							<ListItemText primary={product.name} className="first-field" />
							<ListItemText primary={`in stock: ${product.quantity}`} />
						</ListItem>
					)}
				</GenericList>
				<GenericList
					data={appointees[0].appointees}
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
						/>
					)}
				</GenericList>
				<GenericList data={appointees} header="Store's appointments" narrow>
					{(appointee) => (
						<AppointeeNode
							appointee={appointee}
							isSelected={(appointee) => selectedItem === appointee.username}
							onClick={(appointee) => onSelectAppointee(appointee)}
						/>
					)}
				</GenericList>
				<GenericList data={discounts} header="Discounts" narrow>
					{(discount: Discount) => (
						<DiscountNode discount={discount} onCreate={openDiscountForm} />
					)}
				</GenericList>
				<GenericList data={conditions} header="Users can buy products if" narrow>
					{(condition: Condition) => (
						<ConditionNode condition={condition} onCreate={openConditionForm} />
					)}
				</GenericList>
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
