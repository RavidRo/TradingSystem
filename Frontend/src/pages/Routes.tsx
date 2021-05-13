import React, { FC } from 'react';

import { Redirect, Route, Switch } from 'react-router';
import { Product, ProductQuantity, StoreToSearchedProducts } from '../types';

import Cart from './Cart';
import Home from './Home';
import MyAccount from './MyAccount';
import MyStores from './MyStores';
import Purchase from './Purchase';
import SearchPage from './SearchPage';
import SignIn from './SignIn';
import SignUp from './SignUp';
import StoresView from './StoresView';

type RoutesProps = {
	productsInCart: ProductQuantity[];
	storesToProducts: React.MutableRefObject<StoreToSearchedProducts>;
	handleDeleteProduct: (product: Product | null, storeID: string) => void;
	addProductToPopup: (product: Product, storeID: string) => void;

	signedIn: boolean;
	username: string;
	setSignedIn: (isSignedIn: boolean) => void;
	setUsername: (username: string) => void;
};

const Routes: FC<RoutesProps> = ({
	productsInCart,
	storesToProducts,
	handleDeleteProduct,
	signedIn,
	setSignedIn,
	username,
	setUsername,
	addProductToPopup,
}) => {
	return (
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
				render={(props) => <SearchPage {...props} propsAddProduct={addProductToPopup} />}
			/>
			<Route
				path="/storesView"
				exact
				render={(props) => <StoresView {...props} propsAddProduct={addProductToPopup} />}
			/>
			<Route path="/Purchase" exact component={Purchase} />
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
			{signedIn ? (
				<Route path="/my-account" exact>
					{(props) => <MyAccount {...props} username={username} />}
				</Route>
			) : (
				<Redirect to="/" />
			)}
			<Route render={() => <h1>404: page not found</h1>} />
		</Switch>
	);
};

export default Routes;
