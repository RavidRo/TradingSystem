import React, { useEffect, useState } from 'react';
import logo from '../logo.svg';
import '../styles/App.scss';

function App() {
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
				<img src={logo} className="App-logo" alt="logo" />
				<p>
					Edit <code>src/App.tsx</code> and save to reload.
				</p>
				<p>{cookie}</p>
				<a
					className="App-link"
					href="https://reactjs.org"
					target="_blank"
					rel="noopener noreferrer"
				>
					Learn React
				</a>
			</header>
		</div>
	);
}

export default App;
