import React, { FC, useState } from 'react';
import { Discount, ProductQuantity } from '../../types';
import CreateDiscountForm from '../FormWindows/CreateDiscountForm';
// import '../styles/DiscountsList.scss';
import DiscountNode from './DiscountNode';
import GenericList from './GenericList';

type DiscountsListProps = {
	openTab: (component: FC, selectedItem: string) => void;
	products: ProductQuantity[];
};

const DiscountsList: FC<DiscountsListProps> = ({ openTab, products }) => {
	const [discounts, setDiscounts] = useState<Discount[]>([]);

	const openDiscountForm = () =>
		openTab(
			() => <CreateDiscountForm onSubmit={(name) => console.log(name)} products={products} />,
			''
		);

	return (
		<GenericList data={discounts} header="Discounts" narrow>
			{(discount: Discount) => (
				<DiscountNode discount={discount} onCreate={openDiscountForm} />
			)}
		</GenericList>
	);
};

export default DiscountsList;
