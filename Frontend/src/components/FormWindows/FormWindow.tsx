import React, { FC } from 'react';
import { Button } from '@material-ui/core';

type FormWindowProps = {
	handleSubmit: () => void;
	submitText: string;
	header: string;
};

const FormWindow: FC<FormWindowProps> = ({
	handleSubmit,
	submitText: createText,
	children,
	header,
}) => {
	return (
		<div className="form-cont">
			<h3>{header}</h3>
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
