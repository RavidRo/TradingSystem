import { Table, TableBody, TableCell, TableHead, TableRow } from '@material-ui/core';
import React, { FC, useEffect, useState } from 'react';
import { Offer } from '../types';
import OfferRow from '../components/OfferRow';
import useAPI from '../hooks/useAPI';

type OffersTableProps = {
    username:string,
    isManager:boolean, 
    store_id:string,
};

const OffersTable: FC<OffersTableProps> = ({username, isManager, store_id}) => {

    const dummyOffers:Offer[] = [{id:'1', price:0, status: 'undeclared', product_id: '1', product_name: 'dress', store_name:'shein', store_id:'1', username: username},
						{id:'2', price:10, status: 'awaiting manager approval', product_id: '2', product_name: 'shirt', store_name:'amazon', store_id:'2', username: username}]

    const userOffersObj = useAPI<Offer[]>('/get_user_offers');
    const managerOffersObj = useAPI<Offer[]>('/get_store_offers', {store_id: store_id});
   
    const [offers, setOffers] = useState<Offer[]>([]);
    useEffect(()=>{
        // isManager===false?userOffersObj.request().then(({data, error})=>{
        //     if (!error && data) {
        //         setOffers(data.data);
        //     }
        // }):managerOffersObj.request().then(({data, error})=>{
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
                   isManager={isManager}
                   />
                ))}
            </TableBody>
        </Table>
					
	);
};


export default OffersTable;
