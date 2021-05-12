import React, { FC, useState } from 'react';

import { DecisionRule, DiscountComplex, Operator } from '../../../types';
import ComplexDiscountForm from '../ComplexDiscountForm';
import FormWindow from '../FormWindow';

type EditComplexDiscountFormProps = {
	onSubmit: (discount: DiscountComplex) => void;
	discountToEdit: DiscountComplex;
};

const EditComplexDiscountForm: FC<EditComplexDiscountFormProps> = ({
	onSubmit,
	discountToEdit,
}) => {
	const [operator, setOperator] = useState<Operator>(discountToEdit.type);
	const [decisionRule, setDecisionRule] = useState<DecisionRule | ''>(
		discountToEdit.type === 'xor' ? discountToEdit.decision_rule : ''
	);

	function handleSubmit() {
		if (operator === 'xor') {
			if (decisionRule !== '') {
				onSubmit({
					type: operator,
					decision_rule: decisionRule,
					discounts: [],
					discount_type: 'complex',
				});
			}
		} else {
			onSubmit({
				type: operator,
				discounts: [],
				discount_type: 'complex',
			});
		}
	}
	return (
		<FormWindow handleSubmit={handleSubmit} submitText="Confirm!" header="Edit discount">
			<ComplexDiscountForm
				operator={operator}
				setOperator={setOperator}
				decisionRule={decisionRule}
				setDecisionRule={setDecisionRule}
				defaultDiscount={discountToEdit}
			/>
		</FormWindow>
	);
};

export default EditComplexDiscountForm;
