import { FormControl, InputLabel, MenuItem, Select } from '@material-ui/core';
import React, { FC } from 'react';
import { DecisionRule, DiscountComplex, Operator } from '../../types';

type ComplexDiscountFormProps = {
	operator: Operator | '';
	decisionRule: DecisionRule | '';
	setOperator: (operator: Operator) => void;
	setDecisionRule: (decisionRule: DecisionRule) => void;
	defaultDiscount?: DiscountComplex;
};

const ComplexDiscountForm: FC<ComplexDiscountFormProps> = ({
	operator,
	decisionRule,
	setOperator,
	setDecisionRule,
	defaultDiscount,
}) => {
	const handleOperatorChange = (event: React.ChangeEvent<{ value: unknown }>) => {
		setOperator(event.target.value as Operator);
	};
	const handleDecisionRuleChange = (event: React.ChangeEvent<{ value: unknown }>) => {
		setDecisionRule(event.target.value as DecisionRule);
	};

	return (
		<>
			<FormControl fullWidth margin="normal">
				<InputLabel id="operator-label">Operator</InputLabel>
				<Select
					labelId="operator-label"
					id="operator-select"
					value={operator}
					onChange={handleOperatorChange}
					required
					defaultValue={defaultDiscount?.type}
				>
					<MenuItem value={'max'}>MAX</MenuItem>
					<MenuItem value={'and'}>AND</MenuItem>
					<MenuItem value={'or'}>OR</MenuItem>
					<MenuItem value={'xor'}>XOR</MenuItem>
					<MenuItem value={'add'}>ADD</MenuItem>
				</Select>
			</FormControl>
			{operator === 'xor' && (
				<FormControl fullWidth margin="normal">
					<InputLabel id="decision-rule-label">Decision rule</InputLabel>
					<Select
						labelId="decision-rule-label"
						id="decision-rule-select"
						value={decisionRule}
						onChange={handleDecisionRuleChange}
						required
						defaultValue={
							(defaultDiscount?.type === 'xor' && defaultDiscount?.decision_rule) ||
							''
						}
					>
						<MenuItem value={'first'}>First discount</MenuItem>
						<MenuItem value={'max'}>Maximum value</MenuItem>
						<MenuItem value={'min'}>Minimum value</MenuItem>
					</Select>
				</FormControl>
			)}
		</>
	);
};

export default ComplexDiscountForm;
