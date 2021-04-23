import { IconButton, InputLabel, Paper } from '@material-ui/core';
import AddIcon from '@material-ui/icons/Add';
import RemoveIcon from '@material-ui/icons/Remove';
import React, { FC } from 'react';
import '../styles/IncrementField.scss';

type IncrementFieldProps = {
	onChange: (newValue: number) => void;
	value: number;
};

const IncrementField: FC<IncrementFieldProps> = ({ value, onChange }) => {
	return (
		<Paper component="form" className="quantity">
			<IconButton
				disabled={value <= 0}
				aria-label="remove-one"
				onClick={() => onChange(value - 1)}
			>
				<RemoveIcon className="icon" />
			</IconButton>
			<InputLabel>{value}</InputLabel>
			<IconButton aria-label="add" onClick={() => onChange(value + 1)}>
				<AddIcon className="icon" />
			</IconButton>
		</Paper>
	);
};

export default IncrementField;
