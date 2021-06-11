import React, { FC, useContext, useEffect } from 'react';

import { Container, Paper, Typography } from '@material-ui/core';

import PurchaseHistoryTable from '../components/Lists/PurchaseHistoryTable';
import OffersTable from '../components/OffersTable';
import { UsernameContext } from '../contexts';
import '../styles/MyAccount.scss';
import { useAPI2 } from '../hooks/useAPI';
import { getPurchaseHistory } from '../api';

type MyAccountProps = {};

const MyAccount: FC<MyAccountProps> = () => {
	const { request, data: purchaseHistory } = useAPI2(getPurchaseHistory);

	const username = useContext(UsernameContext);

	useEffect(() => {
		request().then((value) => console.log(value));
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, []);

	return (
		<Container className='account-page-cont'>
			{purchaseHistory && (
				<Paper className='history-cont'>
					<Typography variant='h6' gutterBottom>
						Hello {username} - your purchase history
					</Typography>
					<PurchaseHistoryTable history={purchaseHistory} />
				</Paper>
			)}
			<Paper className='offers-cont'>
				<Typography variant='h6' gutterBottom>
					your offers:
				</Typography>
				<OffersTable isManager={false} store_id={''} />
			</Paper>
		</Container>
	);
};

export default MyAccount;
