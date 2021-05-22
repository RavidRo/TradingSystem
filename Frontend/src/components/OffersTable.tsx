import { Table, TableBody, TableCell, TableHead, TableRow } from '@material-ui/core';
import React, { FC } from 'react';
import { Offer } from '../types';


type OffersTableProps = {
    offers: Offer[],
};

const OffersTable: FC<OffersTableProps> = ({offers}) => {
	

	return (
        <Table size="small" aria-label="purchases">
            <TableHead>
                <TableRow>
                    <TableCell>Product Name</TableCell>
                    <TableCell>Store Name</TableCell>
                    <TableCell>Offered Price</TableCell>
                    <TableCell>Offer status</TableCell>
                </TableRow>
            </TableHead>
            <TableBody>
                {offers.map((offer, index) => (
                    <TableRow key={index}>
                        <TableCell component="th" scope="row">
                            {offer.product_name}
                        </TableCell>
                        <TableCell component="th" scope="row">
                            {offer.store_name}
                        </TableCell>
                        <TableCell component="th" scope="row">
                            {offer.price}
                        </TableCell>
                        <TableCell component="th" scope="row">
                            {offer.status}
                        </TableCell>
                    </TableRow>
                ))}
            </TableBody>
        </Table>
					
	);
};


export default OffersTable;
