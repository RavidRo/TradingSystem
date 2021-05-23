import React, { FC, useEffect, useState } from 'react';

import { Divider, Typography } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';

import useAPI from '../../hooks/useAPI';
import { PurchaseDetails } from '../../types';
import PurchaseHistoryTable from './PurchaseHistoryTable';

const useStyles = makeStyles({
	header: {
		paddingLeft: '16px',
		paddingRight: '16px',
	},
});

type StorePurchaseHistoryProps = {
	storeId: string;
};

const StorePurchaseHistory: FC<StorePurchaseHistoryProps> = ({ storeId }) => {
	const { request } = useAPI<PurchaseDetails[]>('/get_store_purchase_history', {
		store_id: storeId,
	});

	const [history, setHistory] = useState<PurchaseDetails[]>([]);

	useEffect(() => {
		request({}, (data, error) => {
			if (!error && data) {
				setHistory(data.data);
			}
		});
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, []);

	const classes = useStyles();
	return (
		<>
			<Typography className={classes.header}>Purchase History</Typography>
			<Divider />
			<PurchaseHistoryTable history={history} showUsername />
		</>
	);
};

export default StorePurchaseHistory;
