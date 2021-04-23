import { Button, IconButton } from '@material-ui/core';
import CancelIcon from '@material-ui/icons/Close';
import PurchaseIcon from '@material-ui/icons/LocalMall';
import React, { FC, useState } from 'react';
import '../styles/Cart.scss';

import IncrementField from '../components/IncrementField';

type CartProps = {};

const Cart: FC<CartProps> = (props) => {
	const [quantity, setQuantity] = useState<number>(1);
	return (
		<div className="page">
			<div className="order-cont">
				<div className="products-cont">
					<h4>My Cart</h4>
					<span className="line" />
					<div className="product">
						<p>I'm a product </p>
						<IncrementField onChange={setQuantity} value={quantity} />
						<p className="price">$400.00</p>
						<IconButton aria-label="remove">
							<CancelIcon />
						</IconButton>
					</div>
				</div>
				<div className="summary-cont">
					<h4>Order Summary</h4>
					<span className="line" />
					<div className="total-price">
						<h4>Total</h4>
						<h4>$400.00</h4>
					</div>
					<Button
						variant="contained"
						color="secondary"
						className="checkout-button"
						startIcon={<PurchaseIcon />}
					>
						Checkout
					</Button>
				</div>
			</div>
		</div>
	);
};

export default Cart;
