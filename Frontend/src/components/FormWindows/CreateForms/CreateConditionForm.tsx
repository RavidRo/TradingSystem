import React, { FC, useState } from 'react';

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

import {
	ComplexOperator,
	ConditionComplex,
	ConditionObject,
	ConditionSimple,
	Product,
	SimpleOperator,
} from '../../../types';
import FormWindow from '../FormWindow';
// import '../styles/CreateConditionForm.scss';

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

	const handleSimpleOperatorChange = (event: React.ChangeEvent<{ value: unknown }>) => {
		setSimpleOperator(event.target.value as SimpleOperator);
	};
	const handleObjectChange = (event: React.ChangeEvent<{ value: unknown }>) => {
		setConditionObject(event.target.value as ConditionObject);
	};
	const handleIdentifierChange = (event: React.ChangeEvent<{ value: unknown }>) => {
		setConditionIdentifier(event.target.value as string);
	};

	const handleComplexOperatorChange = (event: React.ChangeEvent<{ value: unknown }>) => {
		setComplexOperator(event.target.value as ComplexOperator);
	};

	const set = Array.from(new Set(products.map((product) => product.category)));
	const categories = [...set];

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
					<TextField
						required
						margin="normal"
						id="target"
						fullWidth
						label="Target"
						onChange={(event) => setTarget(event.currentTarget.value)}
						inputMode="numeric"
						type="number"
						error={targetError}
						name="target"
					/>
					<FormControl fullWidth margin="normal">
						<InputLabel id="operator-label">Operator</InputLabel>
						<Select
							labelId="operator-label"
							id="operator-simple"
							value={simpleOperator}
							onChange={handleSimpleOperatorChange}
							required
							name="operator"
						>
							<MenuItem value={'equals'}>Equals to target</MenuItem>
							<MenuItem value={'great-than'}>Greater than target</MenuItem>
							<MenuItem value={'less-than'}>Less than target</MenuItem>
							<MenuItem value={'great-equals'}>Greater or Equals to target</MenuItem>
							<MenuItem value={'less-equals'}>Less or Equals to target</MenuItem>
						</Select>
					</FormControl>
					<FormControl fullWidth margin="normal">
						<InputLabel id="object-label">Context</InputLabel>
						<Select
							labelId="object-label"
							id="object-select"
							value={conditionObject}
							onChange={handleObjectChange}
							required
							name="object"
						>
							<MenuItem value={'product'}>Product</MenuItem>
							<MenuItem value={'category'}>Category</MenuItem>
							<MenuItem value={'bag'}>Bag</MenuItem>
							<MenuItem value={'user'}>User</MenuItem>
						</Select>
					</FormControl>
					{(conditionObject === 'product' || conditionObject === 'category') && (
						<FormControl fullWidth margin="normal">
							<InputLabel id="identifier-label">Identifier</InputLabel>
							<Select
								labelId="identifier-label"
								id="identifier"
								value={conditionIdentifier}
								onChange={handleIdentifierChange}
								required
								name="identifier"
							>
								{conditionObject === 'category'
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
							value={complexOperator}
							onChange={handleComplexOperatorChange}
							required
							name="operator-complex"
						>
							<MenuItem value={'conditional'}>CONDITIONAL</MenuItem>
							<MenuItem value={'and'}>AND</MenuItem>
							<MenuItem value={'or'}>OR</MenuItem>
						</Select>
					</FormControl>
				</div>
			</Fade>
		</FormWindow>
	);
};

export default CreateConditionForm;
