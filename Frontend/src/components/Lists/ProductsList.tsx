import React, { FC } from 'react';

import { IconButton, ListItem, ListItemSecondaryAction, ListItemText } from '@material-ui/core';
import DeleteForeverOutlinedIcon from '@material-ui/icons/DeleteForeverOutlined';

import useAPI from '../../hooks/useAPI';
import { ProductQuantity } from '../../types';
import ProductDetails from '../DetailsWindows/ProductDetails';
import CreateProductForm from '../FormWindows/CreateProductForm';
// import '../styles/ProductsList.scss';
import GenericList from './GenericList';

type ProductsListProps = {
	products: ProductQuantity[];
	setProducts: (newProducts: ProductQuantity[]) => void;
	openTab: (component: FC, selectedItem: string) => void;
	selectedItem: string;
	storeId: string;
};

const ProductsList: FC<ProductsListProps> = ({
	products,
	openTab,
	selectedItem,
	setProducts,
	storeId,
}) => {
	const createProduct = useAPI<{
		cookie: string;
		product_id: string;
	}>('/create_product', {}, 'POST');

	const deleteProductAPI = useAPI<{ cookie: string; answer: string; succeeded: boolean }>(
		'/remove_product_from_store',
		{ store_id: storeId },
		'POST'
	);

	const handleCreateProduct = (
		name: string,
		price: number,
		quantity: number,
		category: string,
		keywords: string[]
	) => {
		createProduct
			.request({
				store_id: storeId,
				name,
				price,
				quantity,
				category,
				keywords,
			})
			.then((createProduct) => {
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

	const openProductForm = () => {
		openTab(() => <CreateProductForm onSubmit={handleCreateProduct} />, '');
	};

	const onSelectProduct = (product: ProductQuantity) => {
		if (product.id !== selectedItem) {
			openTab(() => <ProductDetails product={product} />, product.id);
		}
	};

	const onDelete = (productId: string) => {
		deleteProductAPI.request({ product_id: productId }, (data, error) => {
			if (!error && data !== null) {
				setProducts(products.filter((product) => product.id !== productId));
			}
		});
	};

	return (
		<GenericList
			data={products}
			onCreate={openProductForm}
			header="Products"
			createTxt="+ Add a new product"
			narrow
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
					<ListItemSecondaryAction onClick={() => onDelete(product.id)}>
						<IconButton edge="end" aria-label="delete">
							<DeleteForeverOutlinedIcon />
						</IconButton>
					</ListItemSecondaryAction>
				</ListItem>
			)}
		</GenericList>
	);
};

export default ProductsList;
