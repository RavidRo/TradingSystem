import { GridList, GridListTile } from '@material-ui/core';
import React, { FC, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

import home from '../images/home.jpeg';
import Navbar from './Navbar';
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
			<Navbar/>
			<header className="App-header">
				<p>Cookie: {cookie}</p>
			</header>
			<SearchBar/>
				
			<div className="imgDiv">
			<img 
				className="photo" 
				src={home} 
			/>
			</div>
		</div>
	);
};
export default Home;
