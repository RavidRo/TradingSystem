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
					<Route path="/" exact component={Cart} />
					<Route path="/cart" exact component={Home} />
				</Switch>
			</BrowserRouter>
		</>
	);
}

export default App;
