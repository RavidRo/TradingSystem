import React, { FC, useState } from 'react';
import { ConditionObject, ConditionSimple, Product, SimpleOperator } from '../../../types';
import FormWindow from '../FormWindow';
import SimpleConditionForm from '../SimpleConditionForm';

type EditSimpleConditionFormProps = {
	onSubmit: (condition: ConditionSimple) => void;
	products: Product[];
	conditionToEdit: ConditionSimple;
};

const EditSimpleConditionForm: FC<EditSimpleConditionFormProps> = ({
	onSubmit,
	products,
	conditionToEdit,
}) => {
	const [target, setTarget] = useState<string>('');
	const [simpleOperator, setSimpleOperator] = useState<SimpleOperator | ''>(
		conditionToEdit.operator
	);
	const [conditionObject, setConditionObject] = useState<ConditionObject | ''>(
		conditionToEdit.context.obj
	);
	const [conditionIdentifier, setConditionIdentifier] = useState<string>(
		conditionToEdit.context.obj === 'product' || conditionToEdit.context.obj === 'category'
			? conditionToEdit.context.identifier
			: ''
	);

	const [targetError, setTargetError] = useState<boolean>(false);

	function handleSubmit() {
		setTargetError(+target < 0);
		if (!targetError && target !== '' && simpleOperator !== '' && conditionObject !== '') {
			if (conditionObject === 'product' || conditionObject === 'category') {
				onSubmit({
					target: +target,
					operator: simpleOperator,
					context: { obj: conditionObject, identifier: conditionIdentifier },
				});
			} else {
				onSubmit({
					target: +target,
					operator: simpleOperator,
					context: { obj: conditionObject },
				});
			}
		}
	}
	return (
		<FormWindow handleSubmit={handleSubmit} submitText="Confirm!" header="Edit condition">
			<SimpleConditionForm
				conditionIdentifier={conditionIdentifier}
				conditionObject={conditionObject}
				products={products}
				setConditionIdentifier={setConditionIdentifier}
				setConditionObject={setConditionObject}
				setSimpleOperator={setSimpleOperator}
				setTarget={setTarget}
				simpleOperator={simpleOperator}
				targetError={targetError}
				defaultCondition={conditionToEdit}
			/>
		</FormWindow>
	);
};

export default EditSimpleConditionForm;
