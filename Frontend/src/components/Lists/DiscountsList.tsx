import React, { FC, useEffect, useState } from 'react';

import useAPI from '../../hooks/useAPI';
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
	const getDiscountsAPI = useAPI<Discount>('/get_discounts', { store_id: storeId });
	const addDiscount = useAPI<string>('/add_discount', { store_id: storeId }, 'POST');
	const removeDiscountAPI = useAPI('/remove_discount', { store_id: storeId }, 'POST');
	const editSimpleDiscount = useAPI('/edit_simple_discount', { store_id: storeId }, 'POST');
	const editComplexDiscount = useAPI('/edit_complex_discount', { store_id: storeId }, 'POST');

	const [discounts, setDiscounts] = useState<Discount[]>([]);
	const [rootId, setRootId] = useState<string>('');

	const getDiscounts = () =>
		getDiscountsAPI.request().then((getDiscountsAPI) => {
			if (!getDiscountsAPI.error && getDiscountsAPI.data !== null) {
				setRootId(getDiscountsAPI.data.data.id);
				setDiscounts((getDiscountsAPI.data.data as DiscountComplex).discounts);
			}
		});

	useEffect(() => {
		getDiscounts();
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, []);

	const openDiscountForm = (fatherId: string) => {
		const onAddDiscount = (rule: DiscountSimple | DiscountComplex): void => {
			addDiscount
				.request({
					exist_id: fatherId,
					discount_data: rule,
				})
				.then((addDiscount) => {
					if (!addDiscount.error && addDiscount.data !== null) {
						getDiscounts();
					}
				});
		};

		openTab(() => <CreateDiscountForm onSubmit={onAddDiscount} products={products} />, '');
	};

	const onEditForm = (discount: Discount) => {
		const onEditDiscountSimple = (discountEdited: DiscountSimple) => {
			editSimpleDiscount.request(
				{
					discount_id: discount.id,
					percentage: discountEdited.percentage,
					condition: discountEdited.condition,
					context: discountEdited.context,
				},
				(_, error) => {
					if (!error) {
						getDiscounts();
					}
				}
			);
		};
		const onEditDiscountComplex = (discountEdited: DiscountComplex) => {
			editComplexDiscount.request(
				{
					discount_id: discount.id,
					complex_type: discountEdited.type,
					decision_rule:
						discountEdited.type === 'xor' ? discountEdited.decision_rule : '',
				},
				(_, error) => {
					if (!error) {
						getDiscounts();
					}
				}
			);
		};
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

	const onDelete = (discountId: string) => {
		removeDiscountAPI.request({ discount_id: discountId }, (data, error) => {
			if (!error && data !== null && data.succeeded) {
				getDiscounts();
			}
		});
	};

	const productIdToString = (productId: string) => {
		for (const product of products) {
			if (product.id === productId) {
				return product.name;
			}
		}
		return '';
	};

	return (
		<GenericList
			data={discounts}
			header="Discounts"
			narrow
			createTxt="+ Add discount"
			onCreate={() => openDiscountForm(rootId)}
		>
			{(discount: Discount) => (
				<DiscountNode
					discount={discount}
					onCreate={openDiscountForm}
					onDelete={onDelete}
					productIdToString={productIdToString}
					onEdit={onEditForm}
				/>
			)}
		</GenericList>
	);
};

export default DiscountsList;
