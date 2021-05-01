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
	const getDiscounts = useAPI<Discount>('/get_discounts', { store_id: storeId });
	const addDiscount = useAPI<{ cookie: string; discount_id: string }>(
		'/add_discount',
		{ store_id: storeId },
		'POST'
	);
	const [discounts, setDiscounts] = useState<Discount[]>([]);
	const [rootId, setRootId] = useState<string>('');

	useEffect(() => {
		getDiscounts.request().then((getDiscounts) => {
			if (!getDiscounts.error && getDiscounts.data !== null) {
				setRootId(getDiscounts.data.id);
				setDiscounts((getDiscounts.data.rule as DiscountComplex).operands);
			}
		});
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
						setDiscounts([{ id: addDiscount.data.discount_id, rule }, ...discounts]);
					}
				});
		};

		openTab(() => <CreateDiscountForm onSubmit={onAddDiscount} products={products} />, '');
	};

	return (
		<GenericList data={discounts} header="Discounts" narrow>
			{(discount: Discount) => (
				<DiscountNode discount={discount} onCreate={openDiscountForm} fatherId={rootId} />
			)}
		</GenericList>
	);
};

export default DiscountsList;
