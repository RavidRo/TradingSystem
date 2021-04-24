import React, { FC, useState } from 'react';
import { Button, TextField } from '@material-ui/core';

type CreateProductFormProps = {
	onSubmit: (name: string) => void;
};

const CreateProductForm: FC<CreateProductFormProps> = ({ onSubmit }) => {
	const [name, setName] = useState<string>('');

	function handleSubmit(event: any) {
		onSubmit(name);
		event.preventDefault();
	}
	return (
		<div className="create-store-form-cont">
			<h2>Adding a new product</h2>
			<form className="create-store-form" onSubmit={handleSubmit}>
				<TextField
					required
					margin="normal"
					id="product-name"
					fullWidth
					label="Product's name"
					onChange={(event) => setName(event.currentTarget.value)}
				/>
				<Button type="submit" fullWidth variant="contained" color="primary">
					Add Product!
				</Button>
			</form>
		</div>
	);
};

export default CreateProductForm;
