import React, { FC } from 'react';

import { Redirect, Route, Switch } from 'react-router';
import { Product, StoreToSearchedProducts } from '../types';

import Cart from './Cart';
import Home from './Home';
import MyAccount from './MyAccount';
import MyStores from './MyStores';
import Notifications from './Notifications';
import Purchase from './Purchase';
import SearchPage from './SearchPage';
import SignIn from './SignIn';
import SignUp from './SignUp';
import StoresView from './StoresView';

type RoutesProps = {
	storesToProducts: React.MutableRefObject<StoreToSearchedProducts>;
	handleDeleteProduct: (product: Product | null, storeID: string) => Promise<boolean> | boolean;
	propHandleAdd: (product: Product, storeID: string) => Promise<boolean>;
	changeQuantity: (store: string, product: string, quantity: number) => Promise<boolean>;
	getPropsCookie: () => string;
	propUpdateStores: (map: StoreToSearchedProducts) => void;
	propsAddProduct: (product: Product, storeID: string) => Promise<boolean>;

	signedIn: boolean;
	username: string;
	setSignedIn: (isSignedIn: boolean) => void;
	setUsername: (username: string) => void;
};

const Routes: FC<RoutesProps> = ({
	storesToProducts,
	handleDeleteProduct,
	propHandleAdd,
	changeQuantity,
	getPropsCookie,
	propUpdateStores,

	propsAddProduct,

	signedIn,
	setSignedIn,
	username,
	setUsername,
}) => {
	return (
		<Switch>
			<Route path='/' exact component={Home} />
			<Route
				path='/cart'
				exact
				render={(props) => (
					<Cart
						{...props}
						storesToProducts={storesToProducts.current}
						handleDeleteProduct={handleDeleteProduct}
						propHandleAdd={propHandleAdd}
						changeQuantity={changeQuantity}
						getPropsCookie={getPropsCookie}
						propUpdateStores={propUpdateStores}
					/>
				)}
			/>
			<Route path='/sign-in' exact>
				{() => (
					<SignIn
						onSignIn={(username) => {
							setSignedIn(true);
							setUsername(username);
						}}
					/>
				)}
			</Route>

			<Route path='/sign-up' exact component={SignUp} />
			<Route path='/Notifications' exact component={Notifications} />
			<Route
				path='/searchPage'
				exact
				render={(props) => <SearchPage {...props} propsAddProduct={propsAddProduct} />}
			/>
			<Route
				path='/storesView'
				exact
				render={(props) => <StoresView {...props} propsAddProduct={propsAddProduct} />}
			/>
			<Route path='/Purchase' exact component={Purchase} />
			<Route path='/searchPage' exact component={SearchPage} />
			{signedIn ? (
				<Route
					path='/my-stores'
					exact
					render={(props) => <MyStores {...props} username={username} />}
				/>
			) : (
				<Redirect to='/' />
			)}
			{signedIn ? (
				<Route path='/my-account' exact>
					{(props) => <MyAccount {...props} username={username} />}
				</Route>
			) : (
				<Redirect to='/' />
			)}
			<Route render={() => <h1>404: page not found</h1>} />
		</Switch>
	);
};

export default Routes;
