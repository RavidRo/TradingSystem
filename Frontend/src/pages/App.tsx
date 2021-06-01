import React, { useEffect, useRef, useState } from 'react';
import { BrowserRouter } from 'react-router-dom';
import { createMuiTheme, ThemeProvider } from '@material-ui/core';
import DateFnsUtils from '@date-io/date-fns';

import Navbar from '../components/Navbar';
import Routes from './Routes';

import { Product, StoreToSearchedProducts, notificationTime } from '../types';
import useAPI from '../hooks/useAPI';
import { AdminsContext, CookieContext, UsernameContext } from '../contexts';
import { MuiPickersUtilsProvider } from '@material-ui/pickers';

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
	const [notifications, setNotifications] = useState<notificationTime[]>([]);
	const storesToProducts = useRef<StoreToSearchedProducts>({});

	useEffect(() => {
		getCookie().then((cookie) => {
			if (cookie) {
				const client = new WebSocket('ws://127.0.0.1:5000/connect');
				client.onopen = () => {
					// alert('WebSocket Client Opened');
					client.send(cookie); // have to be here - else socket.receive in server gets stuck
				};
				client.onmessage = (messageEvent) => {
					setNotifications((old) => [
						...old,
						[messageEvent.data, new Date().toUTCString()],
					]);
					// alert('received socket message');
				};
				client.onclose = () => {
					// alert('connection closed!');
				};
			}
		});
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, []);

	const productObj = useAPI<Product[]>('/save_product_in_cart', {}, 'POST');
	const productUpdateObj = useAPI<Product[]>('/change_product_quantity_in_cart', {}, 'POST');

	const addProductToPopup = (product: Product, storeID: string) => {
		let found = false;
		let quantity = 1;
		for (var i = 0; i < Object.values(storesToProducts.current).length; i++) {
			let tuplesArr = Object.values(storesToProducts.current)[i];
			for (var j = 0; j < tuplesArr.length; j++) {
				if (tuplesArr[j][0].id === product.id) {
					quantity = tuplesArr[j][1] + 1;
					found = true;
				}
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
			return productObj
				.request({
					cookie: cookie,
					store_id: storeID,
					product_id: product.id,
					quantity: quantity,
				})
				.then(({ data, error }) => {
					if (!error && data !== null) {
						// do nothing
						return true;
					} else {
						return false;
					}
				});
		} else {
			return productUpdateObj
				.request({
					cookie: cookie,
					store_id: storeID,
					product_id: product.id,
					quantity: quantity,
				})
				.then(({ data, error }) => {
					if (!error && data !== null) {
						let tuplesArr = storesToProducts.current[storeID];
						for (var i = 0; i < tuplesArr.length; i++) {
							if (tuplesArr[i][0].id === product.id) {
								tuplesArr[i][1] += 1;
							}
						}
						storesToProducts.current[storeID] = tuplesArr;
						return true;
					} else {
						return false;
					}
				});
		}
	};

	const propUpdateStores = (map: StoreToSearchedProducts) => {
		storesToProducts.current = map;
	};
	const productQuantityObj = useAPI<void>('/change_product_quantity_in_cart', {}, 'POST');
	const changeQuantity = (storeID: string, productID: string, newQuantity: number) => {
		return productQuantityObj
			.request({
				cookie: cookie,
				store_id: storeID,
				product_id: productID,
				quantity: newQuantity,
			})
			.then(({ data, error }) => {
				if (!error && data !== null) {
					let tuplesArr = storesToProducts.current[storeID];
					for (var i = 0; i < tuplesArr.length; i++) {
						if (tuplesArr[i][0].id === productID) {
							tuplesArr[i][1] = newQuantity;
						}
					}
					storesToProducts.current[storeID] = tuplesArr;
					return true;
				} else {
					return false;
				}
			});
	};
	const getQuantityOfProduct = (productID: string) => {
		for (var i = 0; i < Object.values(storesToProducts.current).length; i++) {
			let tuplesArr = Object.values(storesToProducts.current)[i];
			for (var j = 0; j < tuplesArr.length; j++) {
				if (tuplesArr[j][0].id === productID) {
					return tuplesArr[j][1];
				}
			}
		}
	};

	const productRemoveObj = useAPI<Product[]>('/remove_product_from_cart', {}, 'POST');
	const handleDeleteProduct = (product: Product | null, storeID: string) => {
		if (product !== null) {
			return productRemoveObj
				.request({
					cookie: cookie,
					product_id: product.id,
					store_id: storeID,
					quantity: getQuantityOfProduct(product.id),
				})
				.then(({ data, error }) => {
					if (!error && data !== null) {
						let tupleArr = storesToProducts.current[storeID];
						if (tupleArr.length === 1) {
							// removed the only item from this bag
							tupleArr = [];
						} else {
							let index = 0;
							for (var i = 0; i < tupleArr.length; i++) {
								if (tupleArr[i][0].id === product.id) {
									index = i;
								}
							}
							tupleArr.splice(index, 1);
						}
						storesToProducts.current[storeID] = tupleArr;
						return true;
					} else {
						return false;
					}
				});
		}
		return false;
	};

	const getCookie = () => {
		return request({}).then(({ data, error }) => {
			if (!error && data !== null) {
				setCookie(data.data.cookie);
				return data.data.cookie;
			}
		});
	};

	const getPropsCookie = () => {
		return cookie;
	};

	// useEffect(() => {
	// 	getCookie();
	// 	// eslint-disable-next-line react-hooks/exhaustive-deps
	// }, []);

	return cookie !== '' ? (
		<MuiPickersUtilsProvider utils={DateFnsUtils}>
			<ThemeProvider theme={theme}>
				<CookieContext.Provider value={cookie}>
					<AdminsContext.Provider value={require('../../../config.json').admins}>
						<UsernameContext.Provider value={username}>
							<BrowserRouter>
								<Navbar
									signedIn={signedIn}
									storesToProducts={storesToProducts.current}
									propHandleDelete={handleDeleteProduct}
									notifications={notifications}
									changeQuantity={changeQuantity}
									logout={() => {
										setSignedIn(false);
										setCookie('');
										getCookie();
									}}
									propUpdateStores={propUpdateStores}
								/>
								<Routes
									handleDeleteProduct={handleDeleteProduct}
									setSignedIn={setSignedIn}
									setUsername={setUsername}
									signedIn={signedIn}
									storesToProducts={storesToProducts}
									changeQuantity={changeQuantity}
									getPropsCookie={getPropsCookie}
									propHandleAdd={addProductToPopup}
									propUpdateStores={propUpdateStores}
									propsAddProduct={addProductToPopup}
								/>
							</BrowserRouter>
						</UsernameContext.Provider>
					</AdminsContext.Provider>
				</CookieContext.Provider>
			</ThemeProvider>
		</MuiPickersUtilsProvider>
	) : (
		<h1>LOADING</h1>
	);
}

export default App;
