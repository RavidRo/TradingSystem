module.exports = {
	type: 'react-app',
	devServer: {
		proxy: {
			'/': {
				target: require('../config.json').production
					? 'https://trading-system-workshop.herokuapp.com/'
					: 'http://localhost:5000',
				// pathRewrite: { '^/api': '' },
			},
		},
	},
};
