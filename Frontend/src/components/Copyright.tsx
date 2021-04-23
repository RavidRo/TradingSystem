import { Typography } from '@material-ui/core';
import React, { FC } from 'react';
import { Link } from 'react-router-dom';

import '../styles/copyright.scss';
import config from '../config';
type CopyrightProps = {};

const Copyright: FC<CopyrightProps> = (props) => {
	return (
		<Typography variant="body2" color="textSecondary" align="center">
			{'Copyright © '}
			<Link className="copyright-link" to="/">
				{config.website_name}
			</Link>
			{`${new Date().getFullYear()}.`}
		</Typography>
	);
};

export default Copyright;
