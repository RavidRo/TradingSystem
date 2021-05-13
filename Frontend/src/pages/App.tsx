import React, { useEffect, useRef, useState } from 'react';
import { BrowserRouter } from 'react-router-dom';
import { createMuiTheme, ThemeProvider } from '@material-ui/core';
// import { w3cwebsocket as W3CWebSocket } from 'websocket';

import Navbar from '../components/Navbar';

import { Product, ProductQuantity, StoreToSearchedProducts } from '../types';
import useAPI from '../hooks/useAPI';
import { CookieContext } from '../contexts';
import Routes from './Routes';

const theme = createMuiTheme({
	typography: {
		fontFamily: [
			'Montserrat',
			'-apple-system',
			'BlinkMacSystemFont',
			'"Segoe UI"',
			'Roboto',
			'"Helvetica Neue"',
			'Arial',
			'sans-serif',
			'"Apple Color Emoji"',
			'"Segoe UI Emoji"',
			'"Segoe UI Symbol"',
		].join(','),
	},
	palette: {
		primary: { main: '#fbd1b7' },
		secondary: { main: '#fee9b2' },
	},
});

function App() {
	const [signedIn, setSignedIn] = useState<boolean>(false);
	const [username, setUsername] = useState<string>('Guest');
	const { request } = useAPI<{ cookie: string }>('/get_cookie');
	const [cookie, setCookie] = useState<string>('');
	const [productsInCart, setProducts] = useState<ProductQuantity[]>([]);

	const [notifications, setNotifications] = useState<string[]>([]);

	const storesToProducts = useRef<StoreToSearchedProducts>({});
	// useEffect(() => {
	// 	const client = new W3CWebSocket('ws://127.0.0.1:5000/connect');
	// 	client.onopen = () => {
	// 		console.log('WebSocket Client Connected');
	// 	};
	// 	client.onmessage = (message) => {
	// 		setNotifications((old) => [...old, JSON.stringify(message)]);
	// 	};
	// }, []);

	const productObj = useAPI<Product[]>('/save_product_in_cart', {}, 'POST');
	const productUpdateObj = useAPI<Product[]>('/change_product_quantity_in_cart', {}, 'POST');

	const addProductToPopup = (product: Product, storeID: string) => {
		console.log(storesToProducts);

		let found = false;
		let quantity = 1;
		for (let i = 0; i < Object.values(productsInCart).length; i++) {
			if (Object.values(productsInCart)[i].id === product.id) {
				Object.values(productsInCart)[i].quantity += 1;
				quantity = productsInCart[i].quantity + 1;
				found = true;
			}
		}
		if (!found) {
			let newProduct = {
				id: product.id,
				name: product.name,
				price: product.price,
				quantity: 1,
				category: product.category,
				keywords: product.keywords,
			};
			if (Object.keys(storesToProducts.current).includes(storeID)) {
				let tuplesArr = storesToProducts.current[storeID];
				tuplesArr.push([newProduct, 1]);
			} else {
				storesToProducts.current[storeID] = [[newProduct, 1]];
			}
			console.log(storeID);
			productObj
				.request({
					cookie: cookie,
					store_id: storeID,
					product_id: product.id,
					quantity: quantity,
				})
				.then(({ data, error, errorMsg }) => {
					if (!error && data !== null) {
						// do nothing
						void 0;
					} else {
						// alert(errorMsg);
					}
				});
			setProducts((oldArray) => [...oldArray, newProduct]);
		} else {
			let tuplesArr = storesToProducts.current[storeID];
			for (let i = 0; i < tuplesArr.length; i++) {
				if (tuplesArr[i][0].id === product.id) {
					tuplesArr[i][1] += 1;
				}
			}
			storesToProducts.current[storeID] = tuplesArr;

			productUpdateObj
				.request({
					cookie: cookie,
					store_id: storeID,
					product_id: product.id,
					quantity: quantity,
				})
				.then(({ data, error, errorMsg }) => {
					if (!error && data !== null) {
						// do nothing
						void 0;
					} else {
						// alert(errorMsg);
					}
				});
		}
	};
	const getQuantityOfProduct = (productID: string) => {
		for (var i = 0; i < productsInCart.length; i++) {
			if (productsInCart[i].id === productID) {
				return productsInCart[i].quantity;
			}
		}
	};

	const productRemoveObj = useAPI<Product[]>('/remove_product_from_cart', {}, 'POST');
	const handleDeleteProduct = (product: Product | null, storeID: string) => {
		if (product !== null) {
			productRemoveObj
				.request({
					cookie: cookie,
					product_id: product.id,
					store_id: storeID,
					quantity: getQuantityOfProduct(product.id),
				})
				.then(({ data, error, errorMsg }) => {
					if (!error && data !== null) {
						// do nothing
						void 0;
					}
					// alert(errorMsg);
				});
			setProducts(Object.values(productsInCart).filter((item) => item.id !== product.id));
			let tupleArr = storesToProducts.current[storeID];
			for (var i = 0; i < tupleArr.length; i++) {
				if (tupleArr[i][0].id === product.id) {
					tupleArr[i][1] = 0;
				}
			}
			storesToProducts.current[storeID] = tupleArr;
		}
	};

	const getCookie = () => {
		request({}, (data, error) => {
			if (!error && data !== null) {
				setCookie(data.data.cookie);
			}
		});
	};

	useEffect(() => {
		getCookie();
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, []);

	return cookie !== '' ? (
		<ThemeProvider theme={theme}>
			<CookieContext.Provider value={cookie}>
				<BrowserRouter>
					<Navbar
						signedIn={signedIn}
						products={productsInCart}
						storesToProducts={storesToProducts.current}
						propHandleDelete={handleDeleteProduct}
						propHandleAdd={addProductToPopup}
						notifications={notifications}
						logout={() => {
							setSignedIn(false);
							setCookie('');
							getCookie();
						}}
					/>
					<Routes
						addProductToPopup={addProductToPopup}
						handleDeleteProduct={handleDeleteProduct}
						productsInCart={productsInCart}
						setSignedIn={setSignedIn}
						setUsername={setUsername}
						signedIn={signedIn}
						storesToProducts={storesToProducts}
						username={username}
					/>
				</BrowserRouter>
			</CookieContext.Provider>
		</ThemeProvider>
	) : (
		<h1>LOADING</h1>
	);
}

export default App;
