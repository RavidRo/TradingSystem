import React from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom';

import Home from './Home';
import Cart from './Cart';
import Navbar from './Navbar';

function App() {
	return (
		<>
			<BrowserRouter>
				<Navbar />
				<Switch>
					<Route path="/" exact component={Home} />
					<Route path="/cart" exact component={Cart} />
					<Route path="/searchPage" exact component={Home} />
				</Switch>
			</BrowserRouter>
		</>
	);
}

export default App;
