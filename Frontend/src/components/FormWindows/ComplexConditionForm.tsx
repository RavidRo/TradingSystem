import React, { FC } from 'react';

import { FormControl, InputLabel, MenuItem, Select } from '@material-ui/core';

import { ComplexOperator, ConditionComplex } from '../../types';

type ComplexConditionFormProps = {
	complexOperator: ComplexOperator | '';
	setComplexOperator: (complexOperator: ComplexOperator) => void;
	defaultCondition?: ConditionComplex;
};

const ComplexConditionForm: FC<ComplexConditionFormProps> = ({
	complexOperator,
	setComplexOperator,
	defaultCondition,
}) => {
	const handleComplexOperatorChange = (event: React.ChangeEvent<{ value: unknown }>) => {
		setComplexOperator(event.target.value as ComplexOperator);
	};
	return (
		<FormControl fullWidth margin="normal">
			<InputLabel id="operator-label">Operator</InputLabel>
			<Select
				labelId="operator-label"
				id="operator-select"
				value={complexOperator}
				onChange={handleComplexOperatorChange}
				required
				name="operator-complex"
				defaultValue={defaultCondition?.operator}
			>
				<MenuItem value={'conditional'}>CONDITIONAL</MenuItem>
				<MenuItem value={'and'}>AND</MenuItem>
				<MenuItem value={'or'}>OR</MenuItem>
			</Select>
		</FormControl>
	);
};

export default ComplexConditionForm;
