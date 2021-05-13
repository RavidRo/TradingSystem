import { Container, Paper, Typography } from '@material-ui/core';
import React, { FC, useEffect, useState } from 'react';
import PurchaseHistoryTable from '../components/PurchaseHistoryTable';
import useAPI from '../hooks/useAPI';
import '../styles/MyAccount.scss';
import { PurchaseDetails } from '../types';

type MyAccountProps = {
	username: string;
};

const MyAccount: FC<MyAccountProps> = ({ username }) => {
	const { request } = useAPI<PurchaseDetails[]>('/get_purchase_history');

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
		<Container className="account-page-cont">
			<Paper className="history-cont">
				<Typography variant="h6" gutterBottom>
					Hello {username} - your purchase history
				</Typography>
				<PurchaseHistoryTable history={purchaseHistory} />
			</Paper>
		</Container>
	);
};

export default MyAccount;
