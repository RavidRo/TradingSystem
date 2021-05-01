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
import ConditionNode from './ConditionNode';
import GenericList from './GenericList';

type ConditionsListProps = {
	openTab: (component: FC, selectedItem: string) => void;
	products: ProductQuantity[];
	storeId: string;
};

const ConditionsList: FC<ConditionsListProps> = ({ openTab, products, storeId }) => {
	const getConditionsAPI = useAPI<Condition>('/get_conditions', { store_id: storeId });
	const addCondition = useAPI<{ cookie: string; condition_id: string }>(
		'/add_condition',
		{ store_id: storeId },
		'POST'
	);
	const removeConditionAPI = useAPI<{ cookie: string; answer: string; succeeded: boolean }>(
		'/remove_condition',
		{ store_id: storeId },
		'POST'
	);
	const [rootId, setRootId] = useState<string>('');
	const [conditions, setConditions] = useState<Condition[]>([]);

	const getConditions = () =>
		getConditionsAPI.request().then((getConditionsAPI) => {
			if (!getConditionsAPI.error && getConditionsAPI.data !== null) {
				setRootId(getConditionsAPI.data.id);
				setConditions((getConditionsAPI.data.rule as BasicRule).operands);
			}
		});

	useEffect(() => {
		getConditions();
	}, []);

	const onDelete = (conditionId: string) => {
		removeConditionAPI.request({ condition_id: conditionId }, (data, error) => {
			if (!error && data !== null && data.succeeded) {
				getConditions();
			}
		});
	};

	const openConditionForm = (fatherId: string, conditioning?: 'test' | 'then' | undefined) => {
		const onAddCondition = (rule: ConditionSimple | ConditionComplex): void => {
			addCondition
				.request({
					father_id: fatherId,
					rule,
					conditioning,
				})
				.then((addCondition) => {
					if (!addCondition.error && addCondition.data !== null) {
						getConditions();
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
					onDelete={onDelete}
				/>
			)}
		</GenericList>
	);
};

export default ConditionsList;
