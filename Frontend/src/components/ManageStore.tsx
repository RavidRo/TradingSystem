import React, { FC, useEffect, useState } from 'react';

import { ListItem, ListItemText } from '@material-ui/core';

import { Appointee, Product } from '../types';
import GenericList from './GenericList';
import CreateProductForm from './CreateProductForm';
import ProductDetails from './ProductDetails';
import AppointeeDetails from './AppointeeDetails';
import CreateAppointeeForm from './CreateAppointeeForm';
import AppointeeTree from './AppointeeTree';

type ManageStoreProps = {
	products: Product[];
};

const appointees: Appointee[] = [
	{
		id: '0',
		name: 'Tali',
		role: 'Owner',
		children: [],
	},
	{
		id: '1',
		name: 'Sean',
		role: 'Lover',
		children: [],
	},
];

const ManageStore: FC<ManageStoreProps> = ({ products }) => {
	const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
	const [selectedAppointee, setSelectedAppointee] = useState<Appointee | null>(null);
	const [open, setOpen] = useState<boolean>(false);

	const [Tab, setTab] = useState<FC | null>(null);

	useEffect(() => {
		setOpen(false);
		setSelectedProduct(null);
	}, [products]);

	const onSelectProduct = (product: Product) => {
		setTabAnimation(() => <ProductDetails product={product} />);
	};

	const onSelectAppointee = (appointee: Appointee) => {
		setTabAnimation(() => <AppointeeDetails appointee={appointee} />);
	};

	const openProductForm = () => {
		setTabAnimation(() => <CreateProductForm onSubmit={(name) => console.log(name)} />);
	};

	const openAppointeeForm = () => {
		setTabAnimation(() => <CreateAppointeeForm onSubmit={(name) => console.log(name)} />);
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
				<div className="products-list">
					<GenericList
						data={products}
						onCreate={openProductForm}
						header="Products"
						createTxt="+ Add a new product"
					>
						{(product) => (
							<ListItem
								key={product.id}
								selected={selectedProduct?.id === product.id}
								onClick={() => onSelectProduct(product)}
								button
							>
								<ListItemText primary={product.name} className="first-field" />
								<ListItemText primary={`in stock: ${product.quantity}`} />
							</ListItem>
						)}
					</GenericList>
				</div>
				<div>
					<GenericList
						data={appointees}
						onCreate={openAppointeeForm}
						header="Appointees"
						createTxt="+ Appoint a new member"
					>
						{(appointee) => (
							<ListItem
								key={appointee.id}
								selected={selectedAppointee?.id === appointee.id}
								onClick={() => onSelectAppointee(appointee)}
								button
								alignItems="flex-start"
							>
								<ListItemText
									primary={`${appointee.name} - ${appointee.role}`}
									className="first-field"
								/>
							</ListItem>
						)}
					</GenericList>
				</div>
				<div>
					<AppointeeTree />
				</div>
			</div>
			<div className={'second-tab' + (open ? ' open' : '')}>{Tab && <Tab />}</div>
		</div>
	);
};

export default ManageStore;
