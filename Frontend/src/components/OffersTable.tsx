import { Table, TableBody, TableCell, TableHead, TableRow } from '@material-ui/core';
import React, { FC, useEffect, useState } from 'react';
import { Offer } from '../types';
import OfferRow from '../components/OfferRow';
import useAPI from '../hooks/useAPI';

type OffersTableProps = {
	isManager: boolean;
	store_id: string;
};

const OffersTable: FC<OffersTableProps> = ({ isManager, store_id }) => {
	const userOffersObj = useAPI<Offer[]>('/get_user_offers');
	const managerOffersObj = useAPI<Offer[]>('/get_store_offers', { store_id: store_id });

	const [offers, setOffers] = useState<Offer[]>([]);
	useEffect(() => {
		isManager === false
			? userOffersObj.request().then(({ data, error }) => {
					if (!error && data) {
						setOffers(data.data);
					}
			  })
			: managerOffersObj.request().then(({ data, error }) => {
					if (!error && data) {
						setOffers(data.data);
					}
			  });
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, []);
	return (
		<Table size='small' aria-label='purchases'>
			<TableHead>
				<TableRow>
					<TableCell>Product Name</TableCell>
					<TableCell>Store Name</TableCell>
					<TableCell>Offered Price</TableCell>
					<TableCell>Offer status</TableCell>
				</TableRow>
			</TableHead>
			<TableBody>
				{offers.map((offer) => (
					<OfferRow offer={offer} isManager={isManager} />
				))}
			</TableBody>
		</Table>
	);
};

export default OffersTable;
