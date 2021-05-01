import React, { FC, useState } from 'react';

import { TextField } from '@material-ui/core';

import FormWindow from './FormWindow';

type CreateStoreFormProps = {
	onSubmit: (name: string) => void;
};

const CreateStoreForm: FC<CreateStoreFormProps> = ({ onSubmit }) => {
	const [name, setName] = useState<string>('');

	function handleSubmit() {
		onSubmit(name);
	}
	return (
		<FormWindow handleSubmit={handleSubmit} createText="Open Store!" header="New store">
			<TextField
				required
				margin="normal"
				id="store-name"
				fullWidth
				label="Store's name"
				onChange={(event) => setName(event.currentTarget.value)}
			/>
		</FormWindow>
	);
};

export default CreateStoreForm;
