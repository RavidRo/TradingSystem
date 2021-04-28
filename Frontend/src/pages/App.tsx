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
    const [productsInCart,setProducts] = useState<{name:string,price:number,quantity:number}[]>([]);

	const addProductToPopup = (product:{name:string,price:number})=>{
		let found  = false;
		for(var i=0;i<Object.values(productsInCart).length;i++){
			if(Object.values(productsInCart)[i].name === (product.name)){
				Object.values(productsInCart)[i].quantity+=1;
				found = true;
			}
		}
		if(!found){
			let newProduct = {
				name:product.name,
				price:product.price,
				quantity:1,
			};
			setProducts((old)=>({...old,newProduct}));
		}
	}
	const handleDeleteProduct = (product:{name:string,price:number})=>{
		setProducts(Object.values(productsInCart).filter(item => (item.name !== product.name || item.price !== product.price)));
	}

	return (
		<>
			<ThemeProvider theme={theme}>
				<BrowserRouter>
					<Navbar signedIn={signedIn} products={productsInCart} propHandleDelete={handleDeleteProduct}/>
					<Switch>
						<Route path="/" exact component={Home} />
						<Route path="/cart" exact component={Cart} />
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

						<Route path="/my-stores" exact component={MyStores} />
					</Switch>
				</BrowserRouter>
			</ThemeProvider>
		</>
	);
}

export default App;
