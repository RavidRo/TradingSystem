import React, { FC } from 'react';
import { Button } from '@material-ui/core';

type FormWindowProps = {
	handleSubmit: () => void;
	createText: string;
	header: string;
};

const FormWindow: FC<FormWindowProps> = ({ handleSubmit, createText, children, header }) => {
	return (
		<div className="form-cont">
			<h2>{header}</h2>
			<form
				className="create-form"
				onSubmit={(event: React.FormEvent) => {
					handleSubmit();
					event.preventDefault();
				}}
			>
				{children}
				<Button
					type="submit"
					className="create-btn"
					variant="contained"
					color="primary"
					fullWidth
				>
					{createText}
				</Button>
			</form>
		</div>
	);
};

export default FormWindow;
