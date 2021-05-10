import React, { FC, useEffect, useState } from 'react';
import CartProduct from '../components/CartProduct';
import { Link } from 'react-router-dom';
import '../styles/Bag.scss';
import { ProductQuantity } from '../types';

type BagProps = {
	storeName: string;
	products: ProductQuantity[];
	propHandleDelete: (id: string) => void;
	changeQuantity: (id: string, newQuantity: number) => void;
};

const Bag: FC<BagProps> = ({ storeName, products, propHandleDelete, changeQuantity }: BagProps) => {
	const [productsInCart, setProducts] = useState<ProductQuantity[]>(products);

	useEffect(() => {
		setProducts(products);
	}, [products]);

	const calculateTotal = () => {
		const reducer = (accumulator: number, currentValue: ProductQuantity) =>
			accumulator + currentValue.price * currentValue.quantity;
		return productsInCart.reduce(reducer, 0);
	};
	const [total, setTotal] = useState<number>(calculateTotal());

	const onRemove = (id: string) => {
		setProducts(productsInCart.filter((product) => product.id !== id));
		propHandleDelete(id);
	};
	const onChangeQuantity = (id: string, newQuantity: number) => {
		productsInCart.forEach((product) => {
			if (product.id === id) {
				product.quantity = newQuantity;
				if (newQuantity === 0) {
					onRemove(id);
				}
			}
		});
		setTotal(calculateTotal());
		changeQuantity(id, newQuantity);
	};
	const getQuanOfProduct = (id: string) => {
		for (var i = 0; i < productsInCart.length; i++) {
			if (productsInCart[i].id === id) {
				return productsInCart[i].quantity;
			}
		}
		return 0;
	};

	return (
		<div className="page">
			<div className="order-cont">
				<div className="products-cont">
					<h4>{storeName}</h4>
					<span className="line" />
					{productsInCart.length !== 0 ? (
						productsInCart.map((product) => (
							<CartProduct
								key={product.id}
								product={product}
								quantity={getQuanOfProduct(product.id)}
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
						<h4>Total:</h4>
						<h4>{total}$</h4>
					</div>
					{/* <Button variant="contained" color="secondary" startIcon={<PurchaseIcon />}>
						Checkout
					</Button> */}
				</div>
			</div>
		</div>
	);
};

export default Bag;
