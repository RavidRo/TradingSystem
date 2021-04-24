import React, { FC, useState } from 'react';
import { Button, TextField } from '@material-ui/core';

type CreateStoreFormProps = {
	onSubmit: (name: string) => void;
};

const CreateStoreForm: FC<CreateStoreFormProps> = ({ onSubmit }) => {
	const [name, setName] = useState<string>('');

	function handleSubmit(event: any) {
		onSubmit(name);
		event.preventDefault();
	}
	return (
		<div className="create-store-form-cont">
			<h2>Creating a new store</h2>
			<form className="create-store-form" onSubmit={handleSubmit}>
				<TextField
					required
					margin="normal"
					id="store-name"
					fullWidth
					label="Store's name"
					onChange={(event) => setName(event.currentTarget.value)}
				/>
				<Button type="submit" fullWidth variant="contained" color="primary">
					Create Store!
				</Button>
			</form>
		</div>
	);
};

export default CreateStoreForm;
