import { Paper, Typography } from '@material-ui/core';
import React, { FC } from 'react';
import '../styles/MyAccount.scss';

type MyAccountProps = {
	username: string;
};

const MyAccount: FC<MyAccountProps> = ({ username }) => {
	return (
		<Paper>
			<Typography>Hello {username}</Typography>
		</Paper>
	);
};

export default MyAccount;
