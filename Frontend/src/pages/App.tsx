import React from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom';

import Home from './Home';
import Cart from './Cart';
import Navbar from './Navbar';
import SignIn from './SignIn';
import SignUp from './SignUp';
import SearchPage from './SearchPage';

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

				</Switch>
			</BrowserRouter>
		</>
	);
}

export default App;
