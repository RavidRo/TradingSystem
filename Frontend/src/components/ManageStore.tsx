import React, { FC, useState } from 'react';

import { ListItem, ListItemText } from '@material-ui/core';

import { Product } from '../types';
import GenericList from './GenericList';
import CreateProductForm from './CreateProductForm';
import ProductDetails from './ProductDetails';

type ManageStoreProps = {
	products: Product[];
};

const ManageStore: FC<ManageStoreProps> = ({ products }) => {
	const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
	const [open, setOpen] = useState<boolean>(false);

	const onSelectProduct = (product: Product) => {
		setTab(product);
	};

	const openStoreForm = () => {
		setTab(null);
	};
	const setTab = (product: Product | null) => {
		setOpen(false);
		setTimeout(() => {
			setSelectedProduct(product);
			setOpen(true);
		}, 250);
	};

	return (
		<div className="my-store-page">
			<div className="my-store-cont">
				<div className="products-list">
					<GenericList
						data={products}
						onCreate={openStoreForm}
						header="Products"
						createTxt="+ Add a new product"
					>
						{(product) => (
							<ListItem
								key={product.id}
								selected={selectedProduct?.id === product.id}
								onClick={() => onSelectProduct(product)}
								button
								// className="product-line"
								alignItems="flex-start"
							>
								<ListItemText primary={product.name} className="product-name" />
								<ListItemText primary={`in stock: ${product.quantity}`} />
							</ListItem>
						)}
					</GenericList>
				</div>
				<div>
					<GenericList
						data={[]}
						onCreate={() => {}}
						header="Appointees"
						createTxt="+ Appoint a new member"
					>
						{(appointee) => <ListItemText primary="+ Appoint a new member" />}
					</GenericList>
				</div>
			</div>
			<div className={'second-tab' + (open ? ' open' : '')}>
				{selectedProduct ? (
					<ProductDetails product={selectedProduct} />
				) : (
					<CreateProductForm onSubmit={(name) => console.log(name)} />
				)}
			</div>
		</div>
	);
};

export default ManageStore;
