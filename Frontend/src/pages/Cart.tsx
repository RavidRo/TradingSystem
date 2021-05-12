import React, { FC, useState, useEffect } from 'react';
import '../styles/Cart.scss';
import Bag from '../components/Bag';
import {
	Button,
	Dialog,
	DialogActions,
	DialogContent,
	DialogContentText,
	DialogTitle,
	TextField,
} from '@material-ui/core';
import { Link } from 'react-router-dom';
import {
	Product,
	ProductQuantity,
	ShoppingCart,
	ShoppingBag,
	ProductToQuantity,
	StoreToSearchedProducts,
} from '../types';
import useAPI from '../hooks/useAPI';

type CartProps = {
	products: ProductQuantity[];
	storesToProducts: StoreToSearchedProducts;
	handleDeleteProduct: (product: Product | null, storeID: string) => void;
};

const Cart: FC<CartProps> = ({ products, storesToProducts, handleDeleteProduct }) => {
	const [open, setOpen] = useState<boolean>(false);
	const [age, setAge] = useState<number>(0);
	const [showPurchaseLink, setLink] = useState<boolean>(false);
	// eslint-disable-next-line @typescript-eslint/no-unused-vars
	const [bagsToProducts, setBags] = useState<ShoppingBag[]>([]);
	// eslint-disable-next-line @typescript-eslint/no-unused-vars
	const [storesToProductsMy, setStoresProducts] =
		useState<StoreToSearchedProducts>(storesToProducts);

	const cartObj = useAPI<ShoppingCart>('/get_cart_details');
	useEffect(() => {
		cartObj.request().then(({ data, error, errorMsg }) => {
			if (!error && data !== null) {
				console.log(data.data);
				setBags(data.data.bags);
			} else {
				// alert(errorMsg);
			}
		});
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, []);

	const productQuantityOfTuples = (tuples: ProductToQuantity[]) => {
		let prodQuantities: ProductQuantity[] = tuples.map((tuple) => {
			return {
				id: tuple[0].id,
				name: tuple[0].name,
				category: tuple[0].category,
				price: tuple[0].price,
				keywords: tuple[0].keywords,
				quantity: tuple[1],
			};
		});
		return prodQuantities;
	};

	const calculateTotal = () => {
		let total = 0;
		for (var i = 0; i < Object.keys(storesToProductsMy).length; i++) {
			let priceBag: number = 0;
			for (var j = 0; j < Object.values(storesToProductsMy)[i].length; j++) {
				let productPrice: number = Object.values(storesToProductsMy)[i][j][0].price;
				let productQuantity = Object.values(storesToProductsMy)[i][j][1];
				priceBag += productPrice * productQuantity;
			}
			total += priceBag;
		}
		return total;
	};
	const [totalAmount, setTotalAmount] = useState<number>(calculateTotal());

	const handleDeleteProductMy = (id: string, storeID: string) => {
		let product: Product = {} as Product;
		for (var i = 0; i < Object.keys(storesToProductsMy).length; i++) {
			let tupleArr = Object.values(storesToProductsMy)[i];
			for (var j = 0; j < tupleArr.length; j++) {
				if (tupleArr[i][0].id === id) {
					product = Object.values(storesToProductsMy)[i][j][0];
					tupleArr[i][1] = 0;
					// change product quantity in bag to 0
					Object.values(storesToProductsMy)[i] = tupleArr;
				}
			}
		}
		setTotalAmount(calculateTotal());
		handleDeleteProduct(product, storeID);
	};
	const findBagByProductID = (productID: string) => {
		for (var i = 0; i << Object.keys(storesToProductsMy).length; i++) {
			let tuplesArr = Object.values(storesToProductsMy)[i];
			for (var j = 0; j < tuplesArr.length; j++) {
				if (tuplesArr[j][0].id === productID) {
					return Object.keys(storesToProductsMy)[i];
				}
			}
		}
	};

	const productUpdateObj = useAPI<void>('/change_product_quantity_in_cart', {}, 'POST');
	const changeQuantity = (id: string, newQuantity: number) => {
		for (var i = 0; i < Object.keys(storesToProductsMy).length; i++) {
			let tuplesArr = Object.values(storesToProductsMy)[i];
			for (var j = 0; j < tuplesArr.length; j++) {
				if (tuplesArr[j][0].id === id) {
					Object.values(storesToProductsMy)[i][j][1] = newQuantity;
				}
			}
		}

		setTotalAmount(calculateTotal());

		productUpdateObj
			.request({ store_id: findBagByProductID(id), product_id: id, quantity: newQuantity })
			.then(({ data, error, errorMsg }) => {
				if (!error && data !== null) {
					// do nothing
					void 0;
				} else {
					// alert(errorMsg);
				}
			});
	};
	const discountObj = useAPI<number>('/get_discount', { age: age });
	useEffect(() => {
		if (showPurchaseLink) {
			discountObj.request().then(({ data, error, errorMsg }) => {
				if (!error && data !== null) {
					setTotalAmount(data.data);
				} else {
					// alert(errorMsg);
				}
			});
		}
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [showPurchaseLink]);

	const handleOK = () => {
		setOpen(false);
		setLink(true);
	};
	const handleClick = () => {
		setOpen(true);
	};
	return (
		<div className="cart">
			<h3 className="cartTitle">My Cart:</h3>
			{Object.keys(storesToProductsMy).map((bagID) => {
				return (
					<Bag
						key={bagID}
						// storeName={Object.values(bagIDToName.current)[index].storeName}
						storeName={bagID}
						products={productQuantityOfTuples(storesToProductsMy[bagID])}
						propHandleDelete={(productID: string) =>
							handleDeleteProductMy(productID, bagID)
						}
						changeQuantity={changeQuantity}
					/>
				);
			})}
			<h3 className="totalAmount">Total amount : {totalAmount}</h3>
			<Button
				className="purchaseBtn"
				style={{
					height: '50px',
					fontWeight: 'bold',
					fontSize: 'large',
					border: '#00ffff',
					borderWidth: '4px',
					borderStyle: 'solid',
				}}
				onClick={handleClick}
			>
				Enter Your Age For Discount
			</Button>
			<Dialog open={open} onClose={() => setOpen(false)} aria-labelledby="form-dialog-title">
				<DialogTitle id="form-dialog-title">Enter Your Age</DialogTitle>
				<DialogContent>
					<DialogContentText style={{ fontSize: '20px', color: 'black' }}>
						See if there is a discount available for you
					</DialogContentText>
					<TextField
						autoFocus
						margin="dense"
						id="age"
						label="Age"
						type="number"
						fullWidth
						onChange={(e) => setAge(+e.target.value)}
					/>
				</DialogContent>
				<DialogActions>
					<Button style={{ color: 'blue' }} onClick={() => setOpen(false)}>
						Cancel
					</Button>
					<Button style={{ color: 'blue' }} onClick={() => handleOK()}>
						OK
					</Button>
				</DialogActions>
			</Dialog>
			{showPurchaseLink ? (
				<Link
					className="link"
					to={{
						pathname: '/Purchase',
						state: {
							totalAmount: totalAmount,
						},
					}}
				>
					<button
						className="purchaseBtn"
						style={{
							background: '#7FFF00',
							height: '50px',
							fontWeight: 'bold',
							fontSize: 'large',
							marginTop: '40%',
							marginLeft: '20%',
						}}
						onClick={handleClick}
					>
						Purchase
					</button>
				</Link>
			) : null}
		</div>
	);
};

export default Cart;
