import React, { useEffect, useState } from 'react';
import { BrowserRouter, Switch, Route, Redirect } from 'react-router-dom';
import { createMuiTheme, ThemeProvider } from '@material-ui/core';

import Home from './Home';
import Cart from './Cart';
import Navbar from './Navbar';
import SignIn from './SignIn';
import SignUp from './SignUp';
import MyStores from './MyStores';
import SearchPage from './SearchPage';
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

	useEffect(() => {
		request({}, (data, error) => {
			if (!error && data !== null) {
				setCookie(data.cookie);
			}
		});
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, []);

	return cookie !== '' ? (
		<ThemeProvider theme={theme}>
			<CookieContext.Provider value={cookie}>
				<BrowserRouter>
					<Navbar signedIn={signedIn} />
					<Switch>
						<Route path="/" exact component={Home} />
						<Route path="/cart" exact component={Cart} />
						<Route path="/sign-in" exact>
							{() => <SignIn onSignIn={() => setSignedIn(true)} />}
						</Route>
						<Route path="/sign-up" exact component={SignUp} />
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
