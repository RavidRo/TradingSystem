import React, { FC, useState } from 'react';
import { Condition, ProductQuantity } from '../../types';
import CreateConditionForm from '../FormWindows/CreateConditionForm';
// import '../styles/ConditionsList.scss';
import ConditionNode from './ConditionNode';
import GenericList from './GenericList';

type ConditionsListProps = {
	openTab: (component: FC, selectedItem: string) => void;
	products: ProductQuantity[];
};

const ConditionsList: FC<ConditionsListProps> = ({ openTab, products }) => {
	const [conditions, setConditions] = useState<Condition[]>([]);

	const openConditionForm = () =>
		openTab(
			() => (
				<CreateConditionForm onSubmit={(name) => console.log(name)} products={products} />
			),
			''
		);

	return (
		<GenericList data={conditions} header="Users can buy products if" narrow>
			{(condition: Condition) => (
				<ConditionNode condition={condition} onCreate={openConditionForm} />
			)}
		</GenericList>
	);
};

export default ConditionsList;
