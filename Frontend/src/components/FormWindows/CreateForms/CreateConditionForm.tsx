import React, { FC, useState } from 'react';

import { Fade, FormControl, FormControlLabel, Radio, RadioGroup } from '@material-ui/core';

import {
	ComplexOperator,
	ConditionComplex,
	ConditionObject,
	ConditionSimple,
	Product,
	SimpleOperator,
} from '../../../types';
import FormWindow from '../FormWindow';
import SimpleConditionForm from '../SimpleConditionForm';
import ComplexConditionForm from '../ComplexConditionForm';

type CreateConditionFormProps = {
	onSubmit: (condition: ConditionSimple | ConditionComplex) => void;
	products: Product[];
};

const CreateConditionForm: FC<CreateConditionFormProps> = ({ onSubmit, products }) => {
	const [simple, setSimple] = useState<boolean>(true);
	const [target, setTarget] = useState<string>('');
	const [simpleOperator, setSimpleOperator] = useState<SimpleOperator | ''>('');
	const [conditionObject, setConditionObject] = useState<ConditionObject | ''>('');
	const [conditionIdentifier, setConditionIdentifier] = useState<string>('');

	const [complexOperator, setComplexOperator] = useState<ComplexOperator | ''>('');

	const [targetError, setTargetError] = useState<boolean>(false);

	function handleSubmit() {
		setTargetError(+target < 0);
		if (simple) {
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
		} else if (complexOperator !== '') {
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
	}

	return (
		<FormWindow submitText="Add Condition!" handleSubmit={handleSubmit} header="New condition">
			<FormControl component="fieldset" margin="normal">
				<RadioGroup
					row
					aria-label="position"
					name="position"
					defaultValue="simple"
					onChange={(event) => setSimple(event.currentTarget.value === 'simple')}
				>
					<FormControlLabel
						value="simple"
						control={<Radio color="primary" />}
						label="Simple"
						labelPlacement="top"
					/>
					<FormControlLabel
						value="complex"
						control={<Radio color="primary" />}
						label="Complex"
						labelPlacement="top"
					/>
				</RadioGroup>
			</FormControl>
			<Fade in={simple} unmountOnExit>
				<div style={!simple ? { position: 'absolute' } : {}}>
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
					/>
				</div>
			</Fade>
			<Fade in={!simple} unmountOnExit>
				<div style={simple ? { position: 'absolute' } : {}}>
					<ComplexConditionForm
						complexOperator={complexOperator}
						setComplexOperator={setComplexOperator}
					/>
				</div>
			</Fade>
		</FormWindow>
	);
};

export default CreateConditionForm;
