import { Button } from '@material-ui/core';
import PurchaseIcon from '@material-ui/icons/LocalMall';
import { Link } from 'react-router-dom';
import React, { FC, useState } from 'react';

import '../styles/Cart.scss';
import CartProduct from '../components/CartProduct';
import { Product } from '../types';

const products_data: Product[] = [];

type CartProps = {};

const Cart: FC<CartProps> = (props) => {
	const [products, setProducts] = useState<Product[]>(products_data);
	const onRemove = (id: string) => {
		setProducts(products.filter((product) => product.id !== id));
	};
	const onChangeQuantity = (id: string, newQuantity: number) => {
		products.forEach((product) => {
			if (product.id === id) {
				product.quantity = newQuantity;
			}
		});
	};
	return (
		<div className="page">
			<div className="order-cont">
				<div className="products-cont">
					<h4>My Cart</h4>
					<span className="line" />
					{products.length !== 0 ? (
						products.map((product) => (
							<CartProduct
								key={product.id}
								product={product}
								onRemove={onRemove}
								onChangeQuantity={onChangeQuantity}
							/>
						))
					) : (
						<>
							<h4 className="empty-bag-msg">Your bag is empty</h4>
							<h5>
								You can find products to purchase at the <Link to="/">store</Link>{' '}
							</h5>
						</>
					)}
				</div>
				<div className="summary-cont">
					<h4>Order Summary</h4>
					<span className="line" />
					<div className="total-price">
						<h4>Total</h4>
						<h4>$400.00</h4>
					</div>
					<Button variant="contained" color="secondary" startIcon={<PurchaseIcon />}>
						Checkout
					</Button>
				</div>
			</div>
		</div>
	);
};

export default Cart;
