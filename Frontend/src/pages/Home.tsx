import React, { FC, useEffect, useState } from 'react';

import home from '../images/home.jpeg';
import SearchBar from './SearchBar';
import '../styles/Home.scss';

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
			<header className="App-header">
				<p>Cookie: {cookie}</p>
			</header>
				<SearchBar/>
				<div className="imgDiv">
				<img 
					className="photo" 
					src={home} 
					alt=""
				/>
				</div>
		</div>
	);
};
export default Home;
