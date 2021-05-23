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
import { Product, ShoppingCart, StoreToSearchedProducts, ProductToQuantity } from '../types';
import useAPI from '../hooks/useAPI';
import { useHistory } from 'react-router-dom';
import Swal from 'sweetalert2';

type CartProps = {
	storesToProducts: StoreToSearchedProducts;
	handleDeleteProduct: (product: Product | null, storeID: string) => Promise<boolean> | boolean;
	propHandleAdd: (product: Product, storeID: string) => Promise<boolean>;
	changeQuantity: (store: string, product: string, quan: number) => Promise<boolean>;
	getPropsCookie: () => string;
	propUpdateStores: (map: StoreToSearchedProducts) => void;
};

const Cart: FC<CartProps> = ({
	storesToProducts,
	handleDeleteProduct,
	propHandleAdd,
	changeQuantity,
	getPropsCookie,
	propUpdateStores,
}) => {
	const [open, setOpen] = useState<boolean>(false);
	const [age, setAge] = useState<number>(0);
	const [showPurchaseLink, setLink] = useState<boolean>(false);
	const [storesToProductsMy, setStoresProducts] =
		useState<StoreToSearchedProducts>(storesToProducts);
	const history = useHistory();

	//loas the cart of user when enters the cart page
	const cartObj = useAPI<ShoppingCart>('/get_cart_details');
	const productObj = useAPI<Product>('/get_product');
	useEffect(() => {
		cartObj.request().then(({ data, error }) => {
			if (!error && data !== null) {
				let bags = data.data.bags;
				let map: { [storeID: string]: ProductToQuantity[] } = {};
				let promises: Promise<void>[] = [];
				for (var i = 0; i < bags.length; i++) {
					let bag = bags[i];
					let storeID = bag.store_id;
					let productQuantitiesMap = bag.product_ids_to_quantities;
					let tuplesArr: ProductToQuantity[] = [];
					for (var j = 0; j < Object.keys(productQuantitiesMap).length; j++) {
						let productID: string = Object.keys(productQuantitiesMap)[j];
						let quantity: number = Object.values(productQuantitiesMap)[j];

						let promise = productObj
							.request({ product_id: productID, store_id: storeID })
							.then(({ data, error }) => {
								if (!error && data !== null) {
									let product = data.data;
									tuplesArr.push([product, quantity]);
								}
							});
						promises.push(promise);
					}
					map[storeID] = tuplesArr;
				}
				Promise.allSettled(promises).then(() => {
					setStoresProducts(map);
					propUpdateStores(map);
					setTotalAmount(calculateTotal());
				});
			}
		});
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [storesToProducts]);

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
	const [totalAmount, setTotalAmount] = useState<number>(0);

	//helper function to present products and transfer then to bag
	const productQuantityOfTuples = (bagID: string) => {
		let productsToReturn = [];
		for (var k = 0; k < Object.keys(storesToProductsMy).length; k++) {
			if (Object.keys(storesToProductsMy)[k] === bagID) {
				let tuples = Object.values(storesToProductsMy)[k];
				for (var i = 0; i < tuples.length; i++) {
					let product = {
						id: tuples[i][0].id,
						name: tuples[i][0].name,
						price: tuples[i][0].price,
						category: tuples[i][0].category,
						keywords: tuples[i][0].keywords,
						quantity: tuples[i][1],
					};
					productsToReturn.push(product);
				}
			}
		}

		return productsToReturn;
	};

	//remove product from cart
	const handleDeleteProductMy = (product: Product, storeID: string) => {
		let answer = handleDeleteProduct(product, storeID); //updating server
		if (answer !== false && answer !== true) {
			answer.then((result) => {
				if (result === true) {
					for (var i = 0; i < Object.keys(storesToProductsMy).length; i++) {
						let tupleArr = Object.values(storesToProductsMy)[i];
						for (var j = 0; j < tupleArr.length; j++) {
							if (tupleArr[j][0].id === product.id) {
								// change product quantity in bag to 0
								tupleArr[j][1] = 0;
								Object.values(storesToProductsMy)[i] = tupleArr;
							}
						}
					}
					setTotalAmount(calculateTotal()); //updating amount
				}
			});
		}
		return answer;
	};
	//change quantity of product
	const changeQuantityMy = (storeID: string, prodID: string, newQuantity: number) => {
		let answer = changeQuantity(storeID, prodID, newQuantity); //update server
		answer.then((result) => {
			if (result === true) {
				for (var i = 0; i < Object.keys(storesToProductsMy).length; i++) {
					let tuplesArr = Object.values(storesToProductsMy)[i];
					for (var j = 0; j < tuplesArr.length; j++) {
						if (tuplesArr[j][0].id === prodID) {
							Object.values(storesToProductsMy)[i][j][1] = newQuantity;
						}
					}
				}
				setTotalAmount(calculateTotal());
			}
		});
		return answer;
	};
	const discountObj = useAPI<number>(
		'/purchase_cart',
		{ cookie: getPropsCookie(), age: age },
		'POST'
	);

	const handleOK = () => {
		discountObj.request().then(({ data, error }) => {
			if (!error && data !== null) {
				let prevCost = totalAmount;
				if (data.data < prevCost) {
					alert('Congratulations! You got discount of: ' + (prevCost - data.data));
					setTotalAmount(data.data);
					setLink(true);
				} else {
					alert('No discount for you :(');
					setLink(true);
				}
			}
		});
		setOpen(false);
	};

	const anyItemsInStore = (prodQuanArr: ProductToQuantity[]) => {
		for (var i = 0; i < prodQuanArr.length; i++) {
			if (prodQuanArr[i][1] > 0) {
				//quantity>0
				return true;
			}
		}
		return false;
	};
	const anyItemsInCart = () => {
		for (var i = 0; i < Object.keys(storesToProductsMy).length; i++) {
			if (anyItemsInStore(Object.values(storesToProductsMy)[i])) {
				return true;
			}
		}
		return false;
	};
	const handleClick = () => {
		if (anyItemsInCart()) {
			setOpen(true);
		} else {
			Swal.fire({
				icon: 'error',
				title: 'Oopss...!',
				text: "your can't purchase an empty cart",
			});
		}
	};
	// when pressing + beside the product, update the total amount of the cart
	const handleAddMy = (product: Product, storeID: string) => {
		let answer = propHandleAdd(product, storeID);
		answer.then((result) => {
			if (result === true) {
				setTotalAmount((amount) => amount + product.price);
			}
		});
		return answer;
	};

	const handlePurchase = () => {
		history.push('/Purchase', {
			totalAmount: totalAmount,
			cookie: getPropsCookie(),
		});
	};

	return (
		<div className='cart'>
			<h3 className='cartTitle'>My Cart:</h3>
			{Object.keys(storesToProductsMy).map((bagID) => {
				return (
					<Bag
						key={bagID}
						storeID={bagID}
						products={productQuantityOfTuples(bagID)}
						propHandleDelete={(product: Product) =>
							handleDeleteProductMy(product, bagID)
						}
						propHandleAdd={(product: Product, storeID: string) =>
							handleAddMy(product, storeID)
						}
						changeQuantity={changeQuantityMy}
					/>
				);
			})}
			<h3 className='totalAmount'>Total amount : {totalAmount}</h3>
			<Button
				className='purchaseBtn'
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
			<Dialog open={open} onClose={() => setOpen(false)} aria-labelledby='form-dialog-title'>
				<DialogTitle id='form-dialog-title'>Enter Your Age</DialogTitle>
				<DialogContent>
					<DialogContentText style={{ fontSize: '20px', color: 'black' }}>
						See if there is a discount available for you
					</DialogContentText>
					<TextField
						autoFocus
						margin='dense'
						id='age'
						label='Age'
						type='number'
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
				<button
					className='purchaseBtn'
					style={{
						background: '#7FFF00',
						height: '50px',
						fontWeight: 'bold',
						fontSize: 'large',
					}}
					onClick={handlePurchase}
				>
					Purchase
				</button>
			) : null}
		</div>
	);
};

export default Cart;
