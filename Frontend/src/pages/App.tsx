import React from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom';
import { createMuiTheme, ThemeProvider } from '@material-ui/core';

import Home from './Home';
import Cart from './Cart';
import Navbar from './Navbar';
import SignIn from './SignIn';
import SignUp from './SignUp';
import MyStores from './MyStores';
import SearchPage from './SearchPage';

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
	return (
		<>
			<BrowserRouter>
				<Navbar />
				<Switch>
					<Route path="/" exact component={Home} />
					<Route path="/cart" exact component={Cart} />
					<Route path="/sign-in" exact component={SignIn} />
					<Route path="/sign-up" exact component={SignUp} />
					<Route path="/searchPage" exact component={SearchPage} />
					<Route path="/my-stores" exact component={MyStores} />
				</Switch>
			</BrowserRouter>
		</>
	);
}

export default App;
