import React, { FC, useState } from 'react';
import { ComplexOperator, ConditionComplex } from '../../../types';
import ComplexConditionForm from '../ComplexConditionForm';
import FormWindow from '../FormWindow';

type EditComplexConditionFormProps = {
	onSubmit: (condition: ConditionComplex) => void;
	conditionToEdit: ConditionComplex;
};

const EditComplexConditionForm: FC<EditComplexConditionFormProps> = ({
	onSubmit,
	conditionToEdit,
}) => {
	const [complexOperator, setComplexOperator] = useState<ComplexOperator | ''>(
		conditionToEdit.operator
	);

	const handleSubmit = () => {
		if (complexOperator !== '') {
			if (complexOperator === 'conditional') {
				onSubmit({
					operator: complexOperator,
				});
			} else {
				onSubmit({
					operator: complexOperator,
					children: [],
				});
			}
		}
	};

	return (
		<FormWindow handleSubmit={handleSubmit} submitText="Confirm!" header="Edit condition">
			<ComplexConditionForm
				complexOperator={complexOperator}
				setComplexOperator={setComplexOperator}
				defaultCondition={conditionToEdit}
			/>
		</FormWindow>
	);
};

export default EditComplexConditionForm;
