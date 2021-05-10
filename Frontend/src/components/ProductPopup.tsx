import { TableCell, TableRow } from '@material-ui/core';
import React, { FC, useState } from 'react';
import '../styles/ProductPopup.scss';
import { Product } from '../types';

type ProductPopupProps = {
	id: string;
	name: string;
	price: number;
	quantity: number;
	keywords: string[];
	category: string;
	propHandleDelete: (productID: string) => void;
	propHandleAdd: (product: Product) => void;
};
const PopupCart: FC<ProductPopupProps> = ({
	id,
	name,
	price,
	quantity,
	keywords,
	category,
	propHandleDelete,
	propHandleAdd,
}: ProductPopupProps) => {
	const [prod_quantity, setQuantity] = useState<number>(quantity);
	const handleDelete = () => {
		if (prod_quantity === 1) {
			propHandleDelete(id);
			setQuantity(0);
		} else {
			setQuantity(prod_quantity - 1);
		}
	};
	const handleAddPoup = () => {
		let me = {
			id: id,
			name: name,
			price: price,
			keywords: keywords,
			category: category,
		};
		propHandleAdd(me);
		setQuantity(prod_quantity + 1);
	};
	return prod_quantity > 0 ? (
		<TableRow style={{ alignItems: 'right' }}>
			<TableCell align={'center'}>{name}</TableCell>
			<TableCell align={'center'}>{price * prod_quantity}</TableCell>
			<TableCell align={'center'}>{prod_quantity}</TableCell>
			<TableCell className="buttonsCell">
				<div className="buttons">
					<button className="buttonP" onClick={() => handleAddPoup()}>
						+
					</button>
					<button className="buttonM" onClick={() => handleDelete()}>
						-
					</button>
				</div>
			</TableCell>
		</TableRow>
	) : null;
};

export default PopupCart;
