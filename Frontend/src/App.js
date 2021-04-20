import './styles/App.scss';

import React, { useEffect, useState } from 'react';

const App = () => {
	const [cookie, setCookie] = useState(null);
	useEffect(() => {
		fetch('/cookie').then((response) => {
			response.text().then(setCookie);
			// response.json().then(setCookie);
			console.log(response);
		});
	}, []);
	return (
		<div className="App">
			<div className="App-heading App-flex">
				<h2>
					Welcome to <span className="App-react">Shooping World</span>
				</h2>
				{cookie && <h4>My cookie is {cookie}</h4>}
			</div>
			<div className="App-instructions App-flex">
				<img className="App-logo" src={'./react.svg'} />
				<p>
					Edit <code>src/App.js</code> and save to hot reload your changes.
				</p>
			</div>
		</div>
	);
};

export default App;
