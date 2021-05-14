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
import { Product, ProductQuantity, StoreToSearchedProducts,Store } from '../types';
import useAPI from '../hooks/useAPI';
import { CookieContext } from '../contexts';
import Notifications from '../pages/Notifications';

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

	type storesToProductsMapType = {
		[key: string]: Product[];
	};

	const storesToProducts = useRef<StoreToSearchedProducts>({});
	const storesProducts = useAPI<storesToProductsMapType>('/search_product', {});
	useEffect(() => {
		const client = new W3CWebSocket('ws://127.0.0.1:5000/connect');
		client.onopen = () => {
			alert('WebSocket Client Connected');
		};
		client.onmessage = (message) => {
			setNotifications((old) => [...old, JSON.stringify(message)]);
		};
	}, []);

	const productObj = useAPI<Product[]>('/save_product_in_cart', {}, 'POST');
	const productUpdateObj = useAPI<Product[]>('/change_product_quantity_in_cart', {}, 'POST');

	const addProductToPopup = (product: Product, storeID: string) => {
		let found = false;
		let quantity = 1;
		for (var i = 0; i < Object.values(productsInCart).length; i++) {
			if (Object.values(productsInCart)[i].id === product.id) {
				// Object.values(productsInCart)[i].quantity += 1;
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
			return productObj
				.request({
					cookie: cookie,
					store_id: storeID,
					product_id: product.id,
					quantity: quantity,
				})
				.then(({ data, error, errorMsg }) => {
					if (!error && data !== null) {
						// do nothing
						setProducts((oldArray) => [...oldArray, newProduct]);
						return true;
					} else {
						alert(errorMsg);
						return false;
					}
				});
		}
		else {
			return productUpdateObj
				.request({
					cookie: cookie,
					store_id: storeID,
					product_id: product.id,
					quantity: quantity,
				})
				.then(({ data, error, errorMsg }) => {
					if (!error && data !== null) {
						for (var i = 0; i < Object.values(productsInCart).length; i++) {
							if (Object.values(productsInCart)[i].id === product.id) {
								Object.values(productsInCart)[i].quantity += 1;
							}
						}
						let tuplesArr = storesToProducts.current[storeID];
						for (var i = 0; i < tuplesArr.length; i++) {
							if (tuplesArr[i][0].id === product.id) {
								tuplesArr[i][1] += 1;
							}
						}
						storesToProducts.current[storeID] = tuplesArr;
						return true;
					} 
					else {
						alert(errorMsg);
						return false;
					}
				});
		}
	};
	const productQuantityObj = useAPI<void>('/change_product_quantity_in_cart',{},'POST');
    const changeQuantity = (storeID:string, productID: string, newQuantity: number)=>{
        productQuantityObj.request({cookie:cookie,store_id:storeID,product_id:productID,quantity:newQuantity}).then(({data,error,errorMsg})=>{
            if(!error && data!==null){
				for (var i = 0; i < Object.values(productsInCart).length; i++) {
					if (Object.values(productsInCart)[i].id === productID) {
						Object.values(productsInCart)[i].quantity += 1;
					}
				}
				let tuplesArr = storesToProducts.current[storeID];
				for (var i = 0; i < tuplesArr.length; i++) {
					if (tuplesArr[i][0].id === productID) {
						tuplesArr[i][1]  = newQuantity;
					}
				}
				storesToProducts.current[storeID] = tuplesArr;
				setProducts(productsInCart);
                void(0);
            }
            else{
                alert(errorMsg);
            }
        })
    }
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
						let tupleArr = storesToProducts.current[storeID];
						for (var i = 0; i < tupleArr.length; i++) {
							if (tupleArr[i][0].id === product.id) {
								tupleArr[i][1] = 0;
							}
						}
						storesToProducts.current[storeID] = tupleArr;
						setProducts(Object.values(productsInCart).filter((item) => item.id !== product.id));
					}
					else{
						alert(errorMsg);
					}
				});
			
		}
	};

	const getCookie = () => {
		request({}, (data, error) => {
			if (!error && data !== null) {
				setCookie(data.data.cookie);
			}
		});
	};

	const getPropsCookie = ()=>{
		return cookie;
	}

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
						changeQuantity={changeQuantity}
						logout={() => {
							setSignedIn(false);
							setCookie('');
							getCookie();
						}}
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
									storesToProducts={storesToProducts.current}
									handleDeleteProduct={handleDeleteProduct}
									propHandleAdd={addProductToPopup}								
									changeQuantity={changeQuantity}
									getPropsCookie={getPropsCookie}
								/>
							)}
						/>
						<Route path="/sign-in" exact>
							{() => (
								<SignIn
									onSignIn={(username) => {
										setSignedIn(true);
										setUsername(username);
									}}
								/>
							)}
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
						<Route path="/Notifications" exact component={Notifications} />
						<Route path="/searchPage" exact component={SearchPage} />
						{signedIn ? (
							<Route
								path="/my-stores"
								exact
								render={(props) => <MyStores {...props} username={username} />}
							/>
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
