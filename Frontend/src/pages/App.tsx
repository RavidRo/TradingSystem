import React, { useState } from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom';
import { createMuiTheme, ThemeProvider } from '@material-ui/core';

import Home from './Home';
import Cart from './Cart';
import Navbar from '../components/Navbar';
import SignIn from './SignIn';
import SignUp from './SignUp';
import MyStores from './MyStores';
import SearchPage from './SearchPage';
import StoresView from '../pages/StoresView';
import Purchase from '../pages/Purchase';
import {Product} from '../types';

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
    const [productsInCart,setProducts] = useState<Product[]>([]);

	const addProductToPopup = (product:Product)=>{
		let found  = false;
		for(var i=0;i<Object.values(productsInCart).length;i++){
			if(Object.values(productsInCart)[i].id === (product.id)){
				Object.values(productsInCart)[i].quantity+=1;
				found = true;
			}
		}
		if(!found){
			let newProduct = {
				id:product.id,
				name:product.name,
				price:product.price,
				quantity:1,
				category:product.category,
				keywords:product.keywords
			};
			setProducts(oldArray => [...oldArray, newProduct]);
		}
	}
	const handleDeleteProduct = (product:Product)=>{
		setProducts(Object.values(productsInCart).filter(item => item.id !== product.id));
	}

	return (
		<>
			<ThemeProvider theme={theme}>
				<BrowserRouter>
					<Navbar signedIn={signedIn} products={productsInCart} propHandleDelete={handleDeleteProduct}/>
					<Switch>
						<Route path="/" exact component={Home} />
						<Route 
							path="/cart" 
							exact 
							render={(props) => (
								<Cart {...props} products={productsInCart} />
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
								<StoresView {...props} propsAddProduct={addProductToPopup}/>
							)}
						/>

						<Route path="/my-stores" exact component={MyStores} />
						<Route path="/Purchase" exact component={Purchase} />

					</Switch>
				</BrowserRouter>
			</ThemeProvider>
		</>
	);
}

export default App;
