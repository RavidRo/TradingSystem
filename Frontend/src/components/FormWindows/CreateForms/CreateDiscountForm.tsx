import {
	Fade,
	FormControl,
	FormControlLabel,
	InputLabel,
	MenuItem,
	Radio,
	RadioGroup,
	Select,
	TextField,
} from '@material-ui/core';
import React, { FC, useState } from 'react';
import {
	DecisionRule,
	DiscountComplex,
	DiscountObject,
	DiscountSimple,
	Operator,
	Product,
} from '../../../types';
import FormWindow from '../FormWindow';
// import '../styles/CreateDiscountForm.scss';

type CreateDiscountFormProps = {
	onSubmit: (discount: DiscountSimple | DiscountComplex) => void;
	products: Product[];
};

const CreateDiscountForm: FC<CreateDiscountFormProps> = ({ onSubmit, products }) => {
	const [simple, setSimple] = useState<boolean>(true);
	const [percentage, setPercentage] = useState<string>('');
	const [contextObject, setContextObject] = useState<DiscountObject | ''>('');
	const [contextIdentifier, setContextIdentifier] = useState<string>('');
	const [operator, setOperator] = useState<Operator | ''>('');
	const [decisionRule, setDecisionRule] = useState<DecisionRule | ''>('');

	const [percentageError, setPercentageError] = useState<boolean>(false);

	const set = Array.from(new Set(products.map((product) => product.category)));
	const categories = [...set];

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

	const handleObjectChange = (event: React.ChangeEvent<{ value: unknown }>) => {
		setContextObject(event.target.value as DiscountObject);
	};
	const handleIdentifierChange = (event: React.ChangeEvent<{ value: unknown }>) => {
		setContextIdentifier(event.target.value as string);
	};
	const handleOperatorChange = (event: React.ChangeEvent<{ value: unknown }>) => {
		setOperator(event.target.value as Operator);
	};
	const handleDecisionRuleChange = (event: React.ChangeEvent<{ value: unknown }>) => {
		setDecisionRule(event.target.value as DecisionRule);
	};

	return (
		<FormWindow handleSubmit={handleSubmit} createText="Add discount!" header="New discount">
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
						<TextField
							required
							margin="normal"
							id="percentage"
							fullWidth
							label="Percentage"
							onChange={(event) => setPercentage(event.currentTarget.value)}
							inputMode="numeric"
							type="number"
							error={percentageError}
						/>
						<FormControl fullWidth margin="normal">
							<InputLabel id="object-label">Context</InputLabel>
							<Select
								labelId="object-label"
								id="object-select"
								value={contextObject}
								onChange={handleObjectChange}
								required
							>
								<MenuItem value={'product'}>Product</MenuItem>
								<MenuItem value={'category'}>Category</MenuItem>
								<MenuItem value={'store'}>Store</MenuItem>
							</Select>
						</FormControl>
						{contextObject !== 'store' && contextObject !== '' && (
							<FormControl fullWidth margin="normal">
								<InputLabel id="identifier-label">Identifier</InputLabel>
								<Select
									labelId="identifier-label"
									id="identifier-select"
									value={contextIdentifier}
									onChange={handleIdentifierChange}
									required
								>
									{contextObject === 'category'
										? categories.map((category, index) => (
												<MenuItem key={index} value={category}>
													{category}
												</MenuItem>
										  ))
										: products.map((product, index) => (
												<MenuItem key={index} value={product.id}>
													{product.name}
												</MenuItem>
										  ))}
								</Select>
							</FormControl>
						)}
					</div>
				</Fade>
				<Fade in={!simple} unmountOnExit>
					<div style={simple ? { position: 'absolute' } : {}}>
						<FormControl fullWidth margin="normal">
							<InputLabel id="operator-label">Operator</InputLabel>
							<Select
								labelId="operator-label"
								id="operator-select"
								value={operator}
								onChange={handleOperatorChange}
								required
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
								>
									<MenuItem value={'first'}>First discount</MenuItem>
									<MenuItem value={'max'}>Maximum value</MenuItem>
									<MenuItem value={'min'}>Minimum value</MenuItem>
								</Select>
							</FormControl>
						)}
					</div>
				</Fade>
			</div>
		</FormWindow>
	);
};

export default CreateDiscountForm;
