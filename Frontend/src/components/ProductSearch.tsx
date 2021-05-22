import { Button, Card, CardContent, Typography } from '@material-ui/core';
import React, { FC, useEffect, useState } from 'react';
import '../styles/ProductSearch.scss';
import { Link } from 'react-router-dom';
import useAPI from '../hooks/useAPI';
import { Store } from '../types';

type ProductSearchProps = {
	content: string;
	price: number;
	storeID: string;
	quantity: number;
	category: string;
	keywords: string[];
	clickAddProduct: () => void;
};

const ProductSearch: FC<ProductSearchProps> = ({
	storeID,
	content,
	price,
	quantity,
	category,
	keywords,
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
							}}
							onClick={() => clickAddProduct()}
						>
							Add To Cart
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
