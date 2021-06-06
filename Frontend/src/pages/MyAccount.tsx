import React, { FC, useContext, useEffect, useState } from 'react';

import { Container, Paper, Typography } from '@material-ui/core';

import PurchaseHistoryTable from '../components/Lists/PurchaseHistoryTable';
import OffersTable from '../components/OffersTable';
import { UsernameContext } from '../contexts';
import useAPI from '../hooks/useAPI';
import '../styles/MyAccount.scss';
import { PurchaseDetails } from '../types';

type MyAccountProps = {};

const MyAccount: FC<MyAccountProps> = () => {
	const { request } = useAPI<PurchaseDetails[]>('/get_purchase_history');

	const username = useContext(UsernameContext);

	const [purchaseHistory, setPurchaseHistory] = useState<PurchaseDetails[]>([]);

	useEffect(() => {
		request({}, (data, error) => {
			if (!error && data) {
				setPurchaseHistory(data.data);
			}
		});
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, []);

	return (
		<Container className='account-page-cont'>
			<Paper className='history-cont'>
				<Typography variant='h6' gutterBottom>
					Hello {username} - your purchase history
				</Typography>
				<PurchaseHistoryTable history={purchaseHistory} />
			</Paper>
			{/* {offersObj.data!==null? */}
			<Paper className='offers-cont'>
				<Typography variant='h6' gutterBottom>
					your offers:
				</Typography>
				{/* <OffersTable offers={offersObj.data} /> */}
				<OffersTable isManager={false} store_id={''} />
			</Paper>
			{/* :null} */}
		</Container>
	);
};

export default MyAccount;
