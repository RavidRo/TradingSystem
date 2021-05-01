import React, { FC } from 'react';

import home from '../images/home.jpeg';
import SearchBar from './SearchBar';
import '../styles/Home.scss';

type HomeProps = {};

const Home: FC<HomeProps> = () => {
	return (
		<div className="App">
			<header className="App-header"></header>
			<SearchBar />
			<div className="imgDiv">
				<img className="photo" src={home} alt="" />
			</div>
		</div>
	);
};
export default Home;
