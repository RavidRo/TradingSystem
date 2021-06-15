import React, { FC, useEffect } from 'react';

import {
	addDiscount,
	editComplexDiscount,
	editSimpleDiscount,
	getDiscounts as getDiscountsAPI,
	moveDiscount,
	removeDiscount,
} from '../../api';
import { areYouSure, confirmOnSuccess } from '../../decorators';
import { useAPI2 } from '../../hooks/useAPI';
import {
	Discount,
	DiscountComplex,
	DiscountSimple,
	isDiscountSimple,
	ProductQuantity,
} from '../../types';
import CreateDiscountForm from '../FormWindows/CreateForms/CreateDiscountForm';
import EditComplexDiscountForm from '../FormWindows/EditForms/EditComplexDiscountForm';
import EditSimpleDiscountForm from '../FormWindows/EditForms/EditSimpleDiscountForm';
import DiscountNode from './DiscountNode';
import GenericList from './GenericList';

type DiscountsListProps = {
	openTab: (component: FC, selectedItem: string) => void;
	products: ProductQuantity[];
	storeId: string;
};

const DiscountsList: FC<DiscountsListProps> = ({ openTab, products, storeId }) => {
	const { request: getDiscountsRequest, data: rootDiscount } = useAPI2(getDiscountsAPI);
	const addDiscountAPI = useAPI2(addDiscount);
	const removeDiscountAPI = useAPI2(removeDiscount);
	const editSimpleDiscountAPI = useAPI2(editSimpleDiscount);
	const editComplexDiscountAPI = useAPI2(editComplexDiscount);
	const moveDiscountAPI = useAPI2(moveDiscount);

	const getDiscounts = () => getDiscountsRequest(storeId);

	useEffect(() => {
		getDiscounts();
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, []);

	const openDiscountForm = (fatherId: string) => {
		const onAddDiscount = (rule: DiscountSimple | DiscountComplex): void => {
			addDiscountAPI.request(storeId, rule, fatherId).then(getDiscounts);
		};

		openTab(() => <CreateDiscountForm onSubmit={onAddDiscount} products={products} />, '');
	};

	const onEditForm = (discount: Discount) => {
		const successMessage = 'Discount was edited successfully! \\(v_v)/';
		const onEditDiscountSimple = confirmOnSuccess(
			(discountEdited: DiscountSimple) =>
				editSimpleDiscountAPI
					.request(
						storeId,
						discount.id,
						discountEdited.percentage,
						discountEdited.context,
						discountEdited.condition
					)
					.then(getDiscounts),
			'Edited!',
			successMessage
		);
		const onEditDiscountComplex = confirmOnSuccess(
			(discountEdited: DiscountComplex) =>
				editComplexDiscountAPI
					.request(
						storeId,
						discount.id,
						discountEdited.type,
						discountEdited.type === 'xor' ? discountEdited.decision_rule : undefined
					)
					.then(getDiscounts),
			'Edited!',
			successMessage
		);

		if (isDiscountSimple(discount)) {
			openTab(
				() => (
					<EditSimpleDiscountForm
						onSubmit={onEditDiscountSimple}
						products={products}
						discountToEdit={discount}
					/>
				),
				''
			);
		} else {
			openTab(
				() => (
					<EditComplexDiscountForm
						onSubmit={onEditDiscountComplex}
						discountToEdit={discount}
					/>
				),
				''
			);
		}
	};

	const onDelete = areYouSure(
		(discountId: string) => {
			removeDiscountAPI.request(storeId, discountId).then(getDiscounts);
		},
		"You won't be able to revert this!",
		'Yes, remove discount!'
	);

	const productIdToString = (productId: string) => {
		for (const product of products) {
			if (product.id === productId) {
				return product.name;
			}
		}
		return '';
	};

	const onMove = confirmOnSuccess(
		(srcId: string, destId: string) =>
			moveDiscountAPI.request(storeId, srcId, destId).then(getDiscounts),
		'Moved!',
		'Discount was moved successfully <3'
	);

	const onDrop = (event: React.DragEvent) => {
		event.preventDefault();
		const draggableElementData = event.dataTransfer.getData('text');
		if (rootDiscount) {
			onMove(draggableElementData, rootDiscount.id);
		}
	};

	return (
		rootDiscount && (
			<GenericList
				data={(rootDiscount as DiscountComplex).discounts}
				header='Discounts'
				narrow
				createTxt='+ Add discount'
				onCreate={() => openDiscountForm(rootDiscount.id)}
				onDrop={onDrop}
			>
				{(discount: Discount) => (
					<DiscountNode
						discount={discount}
						onCreate={openDiscountForm}
						onDelete={onDelete}
						productIdToString={productIdToString}
						onEdit={onEditForm}
						onMove={onMove}
					/>
				)}
			</GenericList>
		)
	);
};

export default DiscountsList;
