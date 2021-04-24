import React, { FC, useEffect, useState } from 'react';

import home from '../images/home.jpeg';
import SearchBar from './SearchBar';
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
			<header className="App-header">
				<p>Cookie: {cookie}</p>
			</header>
			<SearchBar />
			<div className="imgDiv">
				<img className="photo" src={home} alt="" />
			</div>
		</div>
	);
};
export default Home;
