import React, { FC, useEffect, useState } from 'react';

import { ListItem, ListItemText } from '@material-ui/core';

import { Appointee, Product, Discount, Condition } from '../types';
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

type ManageStoreProps = {
	products: Product[];
};

const tree: Appointee[] = [
	{
		id: '11',
		name: 'Me',
		role: 'Founder',
		children: [
			{
				id: '12',
				name: 'Sean',
				role: 'Owner',
				children: [
					{
						id: '10',
						name: 'Tali',
						role: 'Owner',
						children: [],
					},
					{
						id: '14',
						name: 'Omer',
						role: 'Manager',
						permissions: {
							appoint_manager: true,
							get_appointments: false,
							get_history: false,
							manage_products: true,
							remove_manager: true,
						},
						children: [],
					},
				],
			},
			{
				id: '13',
				name: 'Inon',
				role: 'Manager',
				children: [],
				permissions: {
					appoint_manager: true,
					get_appointments: false,
					get_history: false,
					manage_products: true,
					remove_manager: true,
				},
			},
		],
	},
];

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

const ManageStore: FC<ManageStoreProps> = ({ products }) => {
	const [selectedItem, setSelectedItem] = useState<string>('');
	const [open, setOpen] = useState<boolean>(false);

	const [Tab, setTab] = useState<FC | null>(null);

	useEffect(() => {
		setOpen(false);
	}, [products]);

	const onSelectProduct = (product: Product) => {
		if (product.id !== selectedItem) {
			setSelectedItem(product.id);
			setTabAnimation(() => <ProductDetails product={product} />);
		}
	};

	const onSelectAppointee = (appointee: Appointee) => {
		if (appointee.id !== selectedItem) {
			setSelectedItem(appointee.id);
			setTabAnimation(() => <AppointeeDetails appointee={appointee} />);
		}
	};

	const openProductForm = () => {
		setSelectedItem('');
		setTabAnimation(() => (
			<CreateProductForm
				onSubmit={(name, number, quantity, category, keywords) => console.log(name)}
			/>
		));
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
					data={tree[0].children}
					onCreate={openAppointeeForm}
					header="My appointees"
					createTxt="+ Appoint a new member"
					narrow
				>
					{(appointee) => (
						<AppointeeNode
							key={appointee.id}
							appointee={appointee}
							isSelected={(appointee) => selectedItem === appointee.id}
							onClick={(appointee) => onSelectAppointee(appointee)}
						/>
					)}
				</GenericList>
				<GenericList data={tree} header="Store's appointments" narrow>
					{(appointee) => (
						<AppointeeNode
							appointee={appointee}
							isSelected={(appointee) => selectedItem === appointee.id}
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
