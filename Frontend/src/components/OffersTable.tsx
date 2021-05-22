import { Table, TableBody, TableCell, TableHead, TableRow } from '@material-ui/core';
import React, { FC, useEffect, useState } from 'react';
import { Offer } from '../types';
import OfferRow from '../components/OfferRow';
import useAPI from '../hooks/useAPI';

type OffersTableProps = {
    username:string,
};

const OffersTable: FC<OffersTableProps> = ({username}) => {

    const dummyOffers:Offer[] = [{id:'1', price:0, status: 'unintiailizes', product_id: '1', product_name: 'dress', store_name:'shein', username: username},
						{id:'2', price:10, status: 'pending', product_id: '2', product_name: 'shirt', store_name:'amazon', username: username}]

    const getOffersObj = useAPI<Offer[]>('/get_user_offers');
    const [offers, setOffers] = useState<Offer[]>([]);
    useEffect(()=>{
        // getOffersObj.request().then(({data, error})=>{
        //     if (!error && data) {
        //         setOffers(data.data);
        //     }
        // })
    }, [])
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
                {dummyOffers.map((offer) => (
                   <OfferRow
                   offer={offer}
                   />
                ))}
            </TableBody>
        </Table>
					
	);
};


export default OffersTable;
