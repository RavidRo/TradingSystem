import React, { FC } from 'react';

import { ListItem, ListItemSecondaryAction, ListItemText } from '@material-ui/core';
import DeleteForeverOutlinedIcon from '@material-ui/icons/DeleteForeverOutlined';
import EditIcon from '@material-ui/icons/Edit';

import { useAPI2 } from '../../hooks/useAPI';
import {
	changeProductQuantity,
	createProduct,
	editProductDetails,
	removeProductFromStore,
} from '../../api';
import { ProductQuantity } from '../../types';
import ProductDetails from '../DetailsWindows/ProductDetails';
import ProductForm from '../FormWindows/ProductForm';
import GenericList from './GenericList';
import SecondaryActionButton from './SecondaryActionButton';
import { areYouSure, confirmOnSuccess, confirm } from '../../decorators';

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
	const createProductAPI = useAPI2(createProduct);
	const deleteProductAPI = useAPI2(removeProductFromStore);
	const editProductAPI = useAPI2(editProductDetails);
	const editProductQuantityAPI = useAPI2(changeProductQuantity);

	const addProduct = (product: ProductQuantity) => {
		setProducts([product, ...products]);
	};
	const editProduct = (editedProduct: ProductQuantity) => {
		setProducts(
			products.map((product) => (product.id === editedProduct.id ? editedProduct : product))
		);
	};

	const handleCreateProduct = (
		name: string,
		price: number,
		quantity: number,
		category: string,
		keywords: string[]
	) => {
		createProductAPI
			.request(storeId, name, price, quantity, category, keywords)
			.then((newProductId) => {
				addProduct({
					id: newProductId,
					name,
					price,
					category,
					keywords,
					quantity,
				});
			});
	};

	const handleEditProduct = confirmOnSuccess(
		(
			id: string,
			name: string,
			price: number,
			quantity: number,
			category: string,
			keywords: string[]
		) => {
			return editProductAPI.request(storeId, id, name, category, price, keywords).then(() => {
				editProduct({
					id,
					category,
					keywords,
					name,
					price,
					quantity: products.find((product) => product.id === id)?.quantity || 0,
				});
				editProductQuantityAPI.request(storeId, id, quantity).then(() => {
					editProduct({
						id,
						category,
						keywords,
						name,
						price,
						quantity,
					});
				});
			});
		},
		'Edited!',
		'The product was edited successfully!'
	);

	const openProductForm = (productToEdit: ProductQuantity | undefined = undefined) => {
		openTab(
			() => (
				<ProductForm
					onSubmit={
						productToEdit
							? (name, price, quantity, category, keywords) =>
									handleEditProduct(
										productToEdit.id,
										name,
										price,
										quantity,
										category,
										keywords
									)
							: handleCreateProduct
					}
					productEditing={productToEdit}
				/>
			),
			''
		);
	};

	const onSelectProduct = (product: ProductQuantity) => {
		if (product.id !== selectedItem) {
			openTab(() => <ProductDetails product={product} />, product.id);
		}
	};

	const onDelete = areYouSure(
		(productId: string) => {
			deleteProductAPI.request(storeId, productId).then(() => {
				setProducts(products.filter((product) => product.id !== productId));
				confirm('Deleted!', 'Product was deleted successfully');
			});
		},
		"You won't be able to revert this!",
		'Yes, delete product!'
	);

	return (
		<GenericList
			data={products}
			onCreate={() => openProductForm()}
			header="Products"
			createTxt="+ Add a new product"
			narrow
		>
			{(product: ProductQuantity) => (
				<ListItem
					key={product.id}
					selected={selectedItem === product.id}
					onClick={() => onSelectProduct(product)}
					button
				>
					<ListItemText primary={product.name} className="first-field" />
					<ListItemText primary={`in stock: ${product.quantity}`} />
					<ListItemSecondaryAction>
						<SecondaryActionButton onClick={() => openProductForm(product)}>
							<EditIcon />
						</SecondaryActionButton>
						<SecondaryActionButton onClick={() => onDelete(product.id)}>
							<DeleteForeverOutlinedIcon />
						</SecondaryActionButton>
					</ListItemSecondaryAction>
				</ListItem>
			)}
		</GenericList>
	);
};

export default ProductsList;
