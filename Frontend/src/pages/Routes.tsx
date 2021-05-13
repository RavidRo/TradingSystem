import React, { FC, useContext } from 'react';

import { Redirect, Route, Switch } from 'react-router';
import { AdminsContext, UsernameContext } from '../contexts';
import { Product, ProductQuantity, StoreToSearchedProducts } from '../types';
import AdminPage from './AdminPage';

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
	setSignedIn: (isSignedIn: boolean) => void;
	setUsername: (username: string) => void;
};

const Routes: FC<RoutesProps> = ({
	productsInCart,
	storesToProducts,
	handleDeleteProduct,
	signedIn,
	setSignedIn,
	setUsername,
	addProductToPopup,
}) => {
	const username = useContext(UsernameContext);
	const admins = useContext(AdminsContext);

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
				<Route path="/my-stores" exact component={MyStores} />
			) : (
				<Redirect to="/" />
			)}
			{signedIn ? (
				<Route path="/my-account" exact component={MyAccount} />
			) : (
				<Redirect to="/" />
			)}
			{signedIn && admins.includes(username) ? (
				<Route path="/admin" exact component={AdminPage} />
			) : (
				<Redirect to="/" />
			)}
			<Route render={() => <h1>404: page not found</h1>} />
		</Switch>
	);
};

export default Routes;
