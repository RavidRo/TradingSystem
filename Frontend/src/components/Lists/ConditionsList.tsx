import React, { FC, useEffect } from 'react';
import {
	addPurchaseRule,
	editPurchaseRule,
	getPurchasePolicy,
	movePurchaseRule,
	removePurchaseRule,
} from '../../api';
import { areYouSure, confirm, confirmOnSuccess } from '../../decorators';

import { useAPI2 } from '../../hooks/useAPI';
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
	const { request: getConditionsRequest, data: rootCondition } = useAPI2(getPurchasePolicy);
	const addConditionAPI = useAPI2(addPurchaseRule);
	const removeConditionAPI = useAPI2(removePurchaseRule);
	const editConditionAPI = useAPI2(editPurchaseRule);
	const moveConditionAPI = useAPI2(movePurchaseRule);

	const productIdToString = (productId: string) => {
		for (const product of products) {
			if (product.id === productId) {
				return product.name;
			}
		}
		return '';
	};

	const getConditions = () => getConditionsRequest(storeId);

	useEffect(() => {
		getConditions();
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, []);

	const onDelete = areYouSure(
		confirmOnSuccess(
			(conditionId: string) =>
				removeConditionAPI.request(storeId, conditionId).then(getConditions),
			'Deleted!',
			'Condition was removed successfully'
		),
		"You won't be able to revert this!",
		'Yes, remove condition!'
	);

	const openConditionForm = (fatherId: string, conditioning?: 'test' | 'then') => {
		const onAddCondition = (rule: ConditionSimple | ConditionComplex) =>
			addConditionAPI
				.request(
					storeId,
					rule,
					isConditionComplex(rule) ? 'complex' : 'simple',
					fatherId,
					conditioning
				)
				.then(() => {
					getConditions();
					confirm('Created!', 'New condition was created successfully (0-0)');
				});
		openTab(() => <CreateConditionForm onSubmit={onAddCondition} products={products} />, '');
	};

	const onEditConditionForm = (condition: Condition) => {
		const successMessage = 'Condition was edited successfully';
		const onEditConditionSimple = confirmOnSuccess(
			(newCondition: ConditionSimple) =>
				editConditionAPI
					.request(storeId, newCondition, condition.id, 'simple')
					.then(getConditions),
			'Edited',
			successMessage
		);
		const onEditConditionComplex = confirmOnSuccess(
			(newCondition: ConditionComplex) =>
				editConditionAPI
					.request(storeId, newCondition, condition.id, 'complex')
					.then(getConditions),
			'Edited!',
			successMessage
		);
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

	const onMove = confirmOnSuccess(
		(conditionId: string, newParentId: string) =>
			moveConditionAPI.request(storeId, conditionId, newParentId).then(getConditions),
		'Move',
		'Condition was moved successfully'
	);

	const onDropRoot = (event: React.DragEvent) => {
		if (rootCondition != null) {
			event.preventDefault();
			const draggableElementData = event.dataTransfer.getData('text');
			onMove(draggableElementData, rootCondition.id);
		}
	};

	return (
		rootCondition && (
			<GenericList
				data={(rootCondition as BasicRule).children}
				header='Users can buy products if:'
				narrow
				onCreate={() => openConditionForm(rootCondition.id)}
				createTxt='+ Add condition'
				onDrop={onDropRoot}
			>
				{(condition: Condition) => (
					<ConditionNode
						condition={condition}
						onCreate={openConditionForm}
						onDelete={onDelete}
						productIdToName={productIdToString}
						onEdit={onEditConditionForm}
						onMove={onMove}
					/>
				)}
			</GenericList>
		)
	);
};

export default ConditionsList;
