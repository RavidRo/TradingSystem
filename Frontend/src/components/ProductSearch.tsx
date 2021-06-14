import { Button, Card, CardContent, Typography } from '@material-ui/core';
import React, { FC, useEffect, useState } from 'react';
import '../styles/ProductSearch.scss';
import { Link } from 'react-router-dom';
import useAPI from '../hooks/useAPI';
import { Store } from '../types';
import Swal from 'sweetalert2';

type ProductSearchProps = {
	content: string;
	price: number;
	storeID: string;
	quantity: number;
	category: string;
	keywords: string[];
	id: string;
	clickAddProduct: () => void;
};

const ProductSearch: FC<ProductSearchProps> = ({
	storeID,
	content,
	price,
	quantity,
	category,
	keywords,
	id,
	clickAddProduct,
}) => {
	const [storeName, setStoreName] = useState<string>('');
	const storeObj = useAPI<Store>('/get_store', { store_id: storeID });
	useEffect(() => {
		if (storeID !== '') {
			storeObj.request().then(({ data, error }) => {
				if (!error && data !== null) {
					setStoreName(data.data.name);
				}
			});
		}
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [storeID]);

	const createOfferObj = useAPI<void>(
		'/create_offer',
		{ store_id: storeID, product_id: id },
		'POST'
	);
	const clickCreateOffer = () => {
		createOfferObj.request().then(({ data, error }) => {
			if (!error && data !== null) {
				Swal.fire({
					icon: 'success',
					title: 'Congratulations!',
					text: 'The item added to offers in "My Account" ',
				});
			}
		});
	};

	return (
		<div className='ProductSearchCard'>
			{content !== '' ? (
				<Card
					className='prodCard'
					style={{
						backgroundColor: '#83f1e8',
					}}
				>
					<CardContent className='cardContent'>
						<Typography style={{ fontSize: 'large', fontWeight: 'bold' }}>
							{content}
						</Typography>
						<Typography style={{ marginTop: '5%' }}>{price}$</Typography>
						<Typography style={{ marginTop: '5%' }}>Quantity: {quantity}</Typography>
						<Typography style={{ marginTop: '5%' }}>Category: {category}</Typography>
						{keywords.length !== 0 ? (
							<Typography style={{ marginTop: '5%' }}>
								Keywords: {keywords}
							</Typography>
						) : null}
					</CardContent>
					<div className='buttonLink'>
						<Button
							style={{
								color: 'blue',
								background: '#ffffff',
								marginTop: '10%',
								padding: '0%',
							}}
							onClick={() => clickAddProduct()}
						>
							Add To Cart
						</Button>
						<Button
							style={{
								color: 'blue',
								background: '#ffffff',
								marginTop: '10%',
								marginLeft: '30%',
								padding: '0%',
							}}
							onClick={() => clickCreateOffer()}
						>
							Add To Offers
						</Button>
						<Link
							className='linkStore'
							to={{
								pathname: '/storesView',
								state: {
									storeID: storeID,
								},
							}}
						>
							{storeName}
						</Link>
					</div>
				</Card>
			) : null}
		</div>
	);
};
export default ProductSearch;
