module.exports = {
	type: 'react-app',
	devServer: {
		proxy: {
			'/': {
				// target: 'http://localhost:5000',
				target: 'https://trading-system-workshop.herokuapp.com/',
				// pathRewrite: { '^/api': '' },
			},
		},
	},
};
