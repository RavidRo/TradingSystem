import React, { FC, useState } from 'react';
import { Button, TextField } from '@material-ui/core';

type CreateAppointeeFormProps = {
	onSubmit: (name: string) => void;
};

const CreateAppointeeForm: FC<CreateAppointeeFormProps> = ({ onSubmit }) => {
	const [name, setName] = useState<string>('');

	function handleSubmit(event: any) {
		onSubmit(name);
		event.preventDefault();
	}
	return (
		<div className="create-store-form-cont">
			<h2>Add a new appointee</h2>
			<form className="create-store-form" onSubmit={handleSubmit}>
				<TextField
					required
					margin="normal"
					id="store-name"
					fullWidth
					label="Store's name"
					onChange={(event) => setName(event.currentTarget.value)}
				/>
				<Button
					type="submit"
					className="create-store-btn"
					variant="contained"
					color="primary"
					fullWidth
				>
					Add appointee!
				</Button>
			</form>
		</div>
	);
};

export default CreateAppointeeForm;
