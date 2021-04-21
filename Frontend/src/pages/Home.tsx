import React, { FC, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

import logo from '../logo.svg';
import Navbar from './Navbar';

type HomeProps = {};

const Home: FC<HomeProps> = () => {
	const [cookie, setCookie] = useState<string>('');
	const getCookie = async () => {
		const response = await fetch('/cookie');
		const newCookie = await response.text();
		setCookie(newCookie);
	};
	useEffect(() => {
		getCookie();
	}, []);
	return (
		<div className="App">
			<Navbar/>
			<header className="App-header">
				<img src={logo} className="App-logo" alt="logo" />
				<p>
					Edit <code>src/App.tsx</code> and save to reload.
				</p>
				<p>{cookie}</p>
				<Link to="/cart" className="App-link">
					My Cart
				</Link>
			</header>
		</div>
	);
};
export default Home;
