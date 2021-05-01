import React, { FC, useEffect, useState } from 'react';
import useAPI from '../../hooks/useAPI';
import {
	BasicRule,
	Condition,
	ConditionComplex,
	ConditionSimple,
	ProductQuantity,
} from '../../types';
import CreateConditionForm from '../FormWindows/CreateConditionForm';
// import '../styles/ConditionsList.scss';
import ConditionNode from './ConditionNode';
import GenericList from './GenericList';

type ConditionsListProps = {
	openTab: (component: FC, selectedItem: string) => void;
	products: ProductQuantity[];
	storeId: string;
};

const ConditionsList: FC<ConditionsListProps> = ({ openTab, products, storeId }) => {
	const getConditions = useAPI<Condition>('/get_conditions', { store_id: storeId });
	const addCondition = useAPI<{ cookie: string; condition_id: string }>(
		'/add_condition',
		{ store_id: storeId },
		'POST'
	);

	const [rootId, setRootId] = useState<string>('');
	const [conditions, setConditions] = useState<Condition[]>([]);

	useEffect(() => {
		getConditions.request().then(() => {
			if (!getConditions.error && getConditions.data !== null) {
				setRootId(getConditions.data.id);
				setConditions((getConditions.data.rule as BasicRule).operands);
			}
		});
	}, []);

	const openConditionForm = (fatherId: string, conditioning?: 'test' | 'then' | undefined) => {
		const onAddCondition = (rule: ConditionSimple | ConditionComplex): void => {
			addCondition
				.request({
					father_id: fatherId,
					rule,
					conditioning,
				})
				.then(() => {
					if (!addCondition.error && addCondition.data !== null) {
						setConditions([
							{ id: addCondition.data.condition_id, rule },
							...conditions,
						]);
					}
				});
		};
		openTab(() => <CreateConditionForm onSubmit={onAddCondition} products={products} />, '');
	};

	return (
		<GenericList data={conditions} header="Users can buy products if" narrow>
			{(condition: Condition) => (
				<ConditionNode
					condition={condition}
					onCreate={openConditionForm}
					fatherId={rootId}
				/>
			)}
		</GenericList>
	);
};

export default ConditionsList;
