import React, { FC, useEffect } from 'react';

import home from '../images/home.jpeg';
import SearchBar from '../components/SearchBar';
import '../styles/Home.scss';
import useAPI from '../hooks/useAPI';

type HomeProps = {};

const Home: FC<HomeProps> = () => {
	const { request: getCookie, data: cookie } = useAPI('/cookie');
	useEffect(() => {
		getCookie();
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, []);

	return (
		<div className="App">
			<SearchBar />
			<p className="mainP">
				Hello, Welcome to Shopping World!
				<br/>
				What can you do here?
				<br/>
				<br/>
				1. Search above for a specific product in your mind
				<br/>
				2. Check out your own cart from the top right
				<br/>
				3. Explore all the stores in the website
				<br/>
				4. Sign in if your already have an account
				<br/>
				<br/>
				So... what are you waiting for ?
			</p>
			<div className="imgDiv">
				<img className="photo" src={home} alt="" />
			</div>
		</div>
	);
};
export default Home;
