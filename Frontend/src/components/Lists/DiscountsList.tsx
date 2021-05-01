import React, { FC, useEffect, useState } from 'react';
import useAPI from '../../hooks/useAPI';
import { Discount, DiscountComplex, DiscountSimple, ProductQuantity } from '../../types';
import CreateDiscountForm from '../FormWindows/CreateDiscountForm';
// import '../styles/DiscountsList.scss';
import DiscountNode from './DiscountNode';
import GenericList from './GenericList';

type DiscountsListProps = {
	openTab: (component: FC, selectedItem: string) => void;
	products: ProductQuantity[];
	storeId: string;
};

const DiscountsList: FC<DiscountsListProps> = ({ openTab, products, storeId }) => {
	const getDiscountsAPI = useAPI<Discount>('/get_discounts', { store_id: storeId });
	const addDiscount = useAPI<{ cookie: string; discount_id: string }>(
		'/add_discount',
		{ store_id: storeId },
		'POST'
	);
	const removeDiscountAPI = useAPI<{ cookie: string; answer: string; succeeded: boolean }>(
		'/remove_discount',
		{ store_id: storeId },
		'POST'
	);
	const [discounts, setDiscounts] = useState<Discount[]>([]);
	const [rootId, setRootId] = useState<string>('');

	const getDiscounts = () =>
		getDiscountsAPI.request().then((getDiscountsAPI) => {
			if (!getDiscountsAPI.error && getDiscountsAPI.data !== null) {
				setRootId(getDiscountsAPI.data.id);
				setDiscounts((getDiscountsAPI.data.rule as DiscountComplex).operands);
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
					fatherId,
					rule,
				})
				.then((addDiscount) => {
					if (!addDiscount.error && addDiscount.data !== null) {
						getDiscounts();
					}
				});
		};

		openTab(() => <CreateDiscountForm onSubmit={onAddDiscount} products={products} />, '');
	};

	const onDelete = (discountId: string) => {
		removeDiscountAPI.request({ discount_id: discountId }, (data, error) => {
			if (!error && data !== null && data.succeeded) {
				getDiscounts();
			}
		});
	};

	return (
		<GenericList data={discounts} header="Discounts" narrow>
			{(discount: Discount) => (
				<DiscountNode
					discount={discount}
					onCreate={openDiscountForm}
					fatherId={rootId}
					onDelete={onDelete}
				/>
			)}
		</GenericList>
	);
};

export default DiscountsList;
