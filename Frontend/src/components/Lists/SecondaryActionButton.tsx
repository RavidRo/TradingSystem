import React, { FC } from 'react';

import { IconButton } from '@material-ui/core';

type SecondaryActionButtonProps = {
	onClick: () => void;
};

const SecondaryActionButton: FC<SecondaryActionButtonProps> = ({ onClick, children }) => {
	return (
		<span className="second-action">
			<IconButton edge="end" onClick={onClick}>
				{children}
			</IconButton>
		</span>
	);
};

export default SecondaryActionButton;
