import React, { FC, useState } from 'react';
import { FormControl, InputLabel, MenuItem, Select, TextField } from '@material-ui/core';
import FormWindow from '../FormWindow';
import { Role } from '../../../types';

type CreateAppointeeFormProps = {
	onSubmit: (appointeeUsername: string, role: Role) => void;
};

const CreateAppointeeForm: FC<CreateAppointeeFormProps> = ({ onSubmit }) => {
	const [role, setRole] = useState<Role | ''>('');
	const [appointeeUsername, setAppointeeUsername] = useState<string>('');

	function handleSubmit() {
		if (role !== '') {
			onSubmit(appointeeUsername, role);
		}
	}

	const handleChange = (event: React.ChangeEvent<{ value: unknown }>) => {
		setRole(event.target.value as Role);
	};

	return (
		<FormWindow createText="Add appointee!" handleSubmit={handleSubmit} header="New appointee">
			<TextField
				required
				margin="normal"
				id="appointee-username"
				fullWidth
				label="Appointee's name"
				onChange={(event) => setAppointeeUsername(event.currentTarget.value)}
			/>
			<FormControl fullWidth margin="normal">
				<InputLabel id="role-label">Role</InputLabel>
				<Select
					labelId="role-label"
					id="role-select"
					value={role}
					onChange={handleChange}
					required
				>
					<MenuItem value={'Manager'}>Manager</MenuItem>
					<MenuItem value={'Owner'}>Owner</MenuItem>
				</Select>
			</FormControl>
		</FormWindow>
	);
};

export default CreateAppointeeForm;
