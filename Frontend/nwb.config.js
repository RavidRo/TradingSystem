module.exports = {
	type: 'react-app',
	devServer: {
		proxy: {
			'/': {
				target: process.env.PRODUCTION
					? 'https://trading-system-workshop.herokuapp.com/'
					: 'http://localhost:5000',
				// pathRewrite: { '^/api': '' },
			},
		},
	},
};
