import React, { FC, useState } from 'react';

import { Fade, FormControl, FormControlLabel, Radio, RadioGroup } from '@material-ui/core';

import {
	DecisionRule,
	DiscountComplex,
	DiscountObject,
	DiscountSimple,
	DiscountComplexType,
	Product,
} from '../../../types';
import FormWindow from '../FormWindow';
import SimpleDiscountForm from '../SimpleDiscountForm';
import ComplexDiscountForm from '../ComplexDiscountForm';

type CreateDiscountFormProps = {
	onSubmit: (discount: DiscountSimple | DiscountComplex) => void;
	products: Product[];
};

const CreateDiscountForm: FC<CreateDiscountFormProps> = ({ onSubmit, products }) => {
	const [simple, setSimple] = useState<boolean>(true);
	const [percentage, setPercentage] = useState<string>('');
	const [contextObject, setContextObject] = useState<DiscountObject | ''>('');
	const [contextIdentifier, setContextIdentifier] = useState<string>('');
	const [operator, setOperator] = useState<DiscountComplexType | ''>('');
	const [decisionRule, setDecisionRule] = useState<DecisionRule | ''>('');

	const [percentageError, setPercentageError] = useState<boolean>(false);

	function handleSubmit() {
		setPercentageError(+percentage < 0);
		if (!percentageError) {
			if (simple && contextObject !== '') {
				if (contextObject === 'store') {
					onSubmit({
						percentage: +percentage,
						context: {
							obj: contextObject,
						},
						discount_type: 'simple',
					});
				} else if (contextIdentifier !== '') {
					onSubmit({
						percentage: +percentage,
						context: {
							obj: contextObject,
							id: contextIdentifier,
						},
						discount_type: 'simple',
					});
				}
			} else {
				if (operator === 'xor') {
					if (decisionRule !== '') {
						onSubmit({
							type: operator,
							decision_rule: decisionRule,
							discounts: [],
							discount_type: 'complex',
						});
					}
				} else if (operator !== '') {
					onSubmit({
						type: operator,
						discounts: [],
						discount_type: 'complex',
					});
				}
			}
		}
	}

	return (
		<FormWindow handleSubmit={handleSubmit} submitText="Add discount!" header="New discount">
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
			<div>
				<Fade in={simple} unmountOnExit>
					<div style={!simple ? { position: 'absolute' } : {}}>
						<SimpleDiscountForm
							contextIdentifier={contextIdentifier}
							contextObject={contextObject}
							percentageError={percentageError}
							products={products}
							setContextIdentifier={setContextIdentifier}
							setContextObject={setContextObject}
							setPercentage={setPercentage}
						/>
					</div>
				</Fade>
				<Fade in={!simple} unmountOnExit>
					<div style={simple ? { position: 'absolute' } : {}}>
						<ComplexDiscountForm
							decisionRule={decisionRule}
							operator={operator}
							setDecisionRule={setDecisionRule}
							setOperator={setOperator}
						/>
					</div>
				</Fade>
			</div>
		</FormWindow>
	);
};

export default CreateDiscountForm;
