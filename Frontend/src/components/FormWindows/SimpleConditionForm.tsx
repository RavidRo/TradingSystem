import React, { FC } from 'react';

import { FormControl, InputLabel, MenuItem, Select, TextField } from '@material-ui/core';

import { ConditionObject, ConditionSimple, Product, SimpleOperator } from '../../types';

type SimpleConditionFormProps = {
	products: Product[];
	setTarget: (target: string) => void;
	targetError: boolean;
	simpleOperator: SimpleOperator | '';
	setSimpleOperator: (simpleOperator: SimpleOperator) => void;
	conditionObject: ConditionObject | '';
	setConditionObject: (conditionObject: ConditionObject) => void;
	conditionIdentifier: string;
	setConditionIdentifier: (conditionIdentifier: string) => void;
	defaultCondition?: ConditionSimple;
};

const SimpleConditionForm: FC<SimpleConditionFormProps> = ({
	products,
	setTarget,
	targetError,
	simpleOperator,
	setSimpleOperator,
	conditionObject,
	setConditionObject,
	conditionIdentifier,
	setConditionIdentifier,
	defaultCondition,
}) => {
	const handleSimpleOperatorChange = (event: React.ChangeEvent<{ value: unknown }>) => {
		setSimpleOperator(event.target.value as SimpleOperator);
	};
	const handleObjectChange = (event: React.ChangeEvent<{ value: unknown }>) => {
		setConditionObject(event.target.value as ConditionObject);
	};
	const handleIdentifierChange = (event: React.ChangeEvent<{ value: unknown }>) => {
		setConditionIdentifier(event.target.value as string);
	};

	const categories = Array.from(new Set(products.map((product) => product.category)));

	return (
		<>
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
				defaultValue={defaultCondition?.target}
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
					defaultValue={defaultCondition?.operator}
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
					defaultValue={defaultCondition?.context.obj}
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
						defaultValue={
							defaultCondition?.context.obj === 'category' ||
							defaultCondition?.context.obj === 'product'
								? defaultCondition?.context.identifier
								: ''
						}
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
		</>
	);
};

export default SimpleConditionForm;
