import React, { useEffect, useRef, useState } from 'react';
import { BrowserRouter, Switch, Route, Redirect } from 'react-router-dom';
import { createMuiTheme, ThemeProvider } from '@material-ui/core';
import { w3cwebsocket as W3CWebSocket } from 'websocket';

import Home from './Home';
import Cart from './Cart';
import Navbar from '../components/Navbar';
import SignIn from './SignIn';
import SignUp from './SignUp';
import MyStores from './MyStores';
import SearchPage from './SearchPage';
import StoresView from '../pages/StoresView';
import Purchase from '../pages/Purchase';
import { Product, ProductQuantity } from '../types';
import useAPI from '../hooks/useAPI';
import { CookieContext } from '../contexts';

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
	const { request } = useAPI<{ cookie: string }>('/get_cookie');
	const [cookie, setCookie] = useState<string>('');
	const [productsInCart, setProducts] = useState<ProductQuantity[]>([]);

	const [notification, setNotification] = useState<string[]>([]);

	type storesToProductsMapType = {
		[key: string]: Product[];
	};

	const storesToProducts = useRef<storesToProductsMapType>({});
	const storesProducts = useAPI<storesToProductsMapType>('/search_product', {});
	useEffect(() => {
		// const client = new W3CWebSocket('ws://127.0.0.1:8000');
		// client.onopen = () => {
		// 	console.log('WebSocket Client Connected');
		//   };
		//   client.onmessage = (message) => {
		// 	setNotification(old=>[...old,JSON.stringify(message)]);
		//   };
		// storesProducts.request().then(({data,error,errorMsg})=>{
		//     if(!storesProducts.error && storesProducts.data!==null){
		//         storesToProducts.current = storesProducts.data;
		//     }
		// })
	}, []);

	const getStoreByProductID = (id: string) => {
		for (var i = 0; i < Object.keys(storesToProducts).length; i++) {
			for (var j = 0; j < Object.values(storesToProducts)[i].length; j++) {
				if (Object.values(storesToProducts)[i][j].id === id) {
					return Object.keys(storesToProducts)[i];
				}
			}
		}
	};
	const productObj = useAPI<Product[]>('/save_product_in_cart', {}, 'POST');
	const productUpdateObj = useAPI<Product[]>('/change_product_quantity_in_cart', {}, 'POST');

	const addProductToPopup = (product: Product) => {
		let found = false;
		let quantity = 1;
		for (var i = 0; i < Object.values(productsInCart).length; i++) {
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
			setProducts((oldArray) => [...oldArray, newProduct]);
			productObj
				.request({
					store_id: getStoreByProductID(product.id),
					product_id: product.id,
					quantity: quantity,
				})
				.then(({ data, error, errorMsg }) => {
					if (!productObj.error && productObj.data !== null) {
						// do nothing
						void 0;
					}
				});
		} else {
			productUpdateObj
				.request({
					store_id: getStoreByProductID(product.id),
					product_id: product.id,
					quantity: quantity,
				})
				.then(({ data, error, errorMsg }) => {
					if (!productUpdateObj.error && productUpdateObj.data !== null) {
						// do nothing
						void 0;
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
	const handleDeleteProduct = (product: Product | null) => {
		if (product !== null) {
			productRemoveObj
				.request({ product_id: product.id, quantity: getQuantityOfProduct(product.id) })
				.then(({ data, error, errorMsg }) => {
					if (!productRemoveObj.error && productRemoveObj.data !== null) {
						// do nothing
						void 0;
					}
				});
			setProducts(Object.values(productsInCart).filter((item) => item.id !== product.id));
		}
	};

	useEffect(() => {
		request({}, (data, error) => {
			if (!error && data !== null) {
				setCookie(data.data.cookie);
			}
		});
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, []);

	return cookie !== '' ? (
		<ThemeProvider theme={theme}>
			<CookieContext.Provider value={cookie}>
				<BrowserRouter>
					<Navbar
						signedIn={signedIn}
						products={productsInCart}
						propHandleDelete={handleDeleteProduct}
						notification={notification}
					/>
					<Switch>
						<Route path="/" exact component={Home} />
						<Route
							path="/cart"
							exact
							render={(props) => (
								<Cart
									{...props}
									products={productsInCart}
									handleDeleteProduct={handleDeleteProduct}
								/>
							)}
						/>
						<Route path="/sign-in" exact>
							{() => <SignIn onSignIn={() => setSignedIn(true)} />}
						</Route>
						<Route path="/sign-up" exact component={SignUp} />
						<Route
							path="/searchPage"
							exact
							render={(props) => (
								<SearchPage {...props} propsAddProduct={addProductToPopup} />
							)}
						/>
						<Route
							path="/storesView"
							exact
							render={(props) => (
								<StoresView {...props} propsAddProduct={addProductToPopup} />
							)}
						/>
						<Route path="/Purchase" exact component={Purchase} />
						<Route path="/searchPage" exact component={SearchPage} />
						{signedIn ? (
							<Route path="/my-stores" exact component={MyStores} />
						) : (
							<Redirect to="/" />
						)}
						<Route render={() => <h1>404: page not found</h1>} />
					</Switch>
				</BrowserRouter>
			</CookieContext.Provider>
		</ThemeProvider>
	) : (
		<h1>LOADING</h1>
	);
}

export default App;
