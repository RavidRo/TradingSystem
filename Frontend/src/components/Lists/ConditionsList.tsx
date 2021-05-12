import React, { FC, useEffect, useState } from 'react';

import useAPI from '../../hooks/useAPI';
import {
	BasicRule,
	Condition,
	ConditionComplex,
	ConditionSimple,
	isConditionComplex,
	ProductQuantity,
} from '../../types';
import CreateConditionForm from '../FormWindows/CreateForms/CreateConditionForm';
import EditComplexConditionForm from '../FormWindows/EditForms/EditComplexConditionForm';
import EditSimpleConditionForm from '../FormWindows/EditForms/EditSimpleConditionForm';
import ConditionNode from './ConditionNode';
import GenericList from './GenericList';

type ConditionsListProps = {
	openTab: (component: FC, selectedItem: string) => void;
	products: ProductQuantity[];
	storeId: string;
};

const ConditionsList: FC<ConditionsListProps> = ({ openTab, products, storeId }) => {
	const getConditionsAPI = useAPI<Condition>('/get_purchase_policy', { store_id: storeId });
	const addCondition = useAPI<string>('/add_purchase_rule', { store_id: storeId }, 'POST');
	const removeConditionAPI = useAPI('/remove_purchase_rule', { store_id: storeId }, 'POST');
	const editConditionAPI = useAPI('/edit_purchase_rule', { store_id: storeId }, 'POST');

	const [rootId, setRootId] = useState<string>('');
	const [conditions, setConditions] = useState<Condition[]>([]);

	const productIdToString = (productId: string) => {
		for (const product of products) {
			if (product.id === productId) {
				return product.name;
			}
		}
		return '';
	};

	const getConditions = () =>
		getConditionsAPI.request().then((getConditionsAPI) => {
			if (!getConditionsAPI.error && getConditionsAPI.data !== null) {
				setRootId(getConditionsAPI.data.data.id);
				setConditions((getConditionsAPI.data.data as BasicRule).children);
			}
		});

	useEffect(() => {
		getConditions();
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, []);

	const onDelete = (conditionId: string) => {
		removeConditionAPI.request({ rule_id: conditionId }, (data, error) => {
			if (!error && data !== null && data.succeeded) {
				getConditions();
			}
		});
	};

	const openConditionForm = (fatherId: string, conditioning?: 'test' | 'then' | undefined) => {
		const onAddCondition = (rule: ConditionSimple | ConditionComplex): void => {
			addCondition
				.request({
					parent_id: fatherId,
					rule_details: rule,
					clause: conditioning,
					rule_type: isConditionComplex(rule) ? 'complex' : 'simple',
				})
				.then((addCondition) => {
					if (!addCondition.error && addCondition.data !== null) {
						getConditions();
					}
				});
		};
		openTab(() => <CreateConditionForm onSubmit={onAddCondition} products={products} />, '');
	};

	const onEditConditionForm = (condition: Condition) => {
		const onEditConditionSimple = (newCondition: ConditionSimple) => {
			editConditionAPI.request(
				{ rule_type: 'simple', rule_id: condition.id, rule_details: newCondition },
				(_, error) => {
					if (!error) {
						getConditions();
					}
				}
			);
		};
		const onEditConditionComplex = (newCondition: ConditionComplex) => {
			editConditionAPI.request(
				{ rule_type: 'complex', rule_id: condition.id, rule_details: newCondition },
				(_, error) => {
					if (!error) {
						getConditions();
					}
				}
			);
		};
		if (isConditionComplex(condition)) {
			openTab(
				() => (
					<EditComplexConditionForm
						onSubmit={onEditConditionComplex}
						conditionToEdit={condition}
					/>
				),
				''
			);
		} else {
			openTab(
				() => (
					<EditSimpleConditionForm
						onSubmit={onEditConditionSimple}
						conditionToEdit={condition}
						products={products}
					/>
				),
				''
			);
		}
	};

	return (
		<GenericList
			data={conditions}
			header="Users can buy products if:"
			narrow
			onCreate={() => openConditionForm(rootId)}
			createTxt="+ Add condition"
		>
			{(condition: Condition) => (
				<ConditionNode
					condition={condition}
					onCreate={openConditionForm}
					onDelete={onDelete}
					productIdToName={productIdToString}
					onEdit={onEditConditionForm}
				/>
			)}
		</GenericList>
	);
};

export default ConditionsList;
