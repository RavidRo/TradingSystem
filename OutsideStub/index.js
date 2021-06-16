const express = require('express');
const app = express();

app.use(express.json()); // to support JSON-encoded bodies
app.use(
	express.urlencoded({
		extended: true,
	})
); // to support URL-encoded bodies

app.post('/', function (req, res) {
	const actionType = req.body.action_type;
	if (actionType === 'handshake') {
		res.send('OK');
	} else if (actionType === 'pay') {
		res.send('20000');
	} else if (actionType === 'cancel_pay') {
		res.send('1');
	} else if (actionType === 'supply') {
		res.send('20000');
	} else if (actionType === 'cancel_supply') {
		res.send('1');
	} else {
		res.status(400).send('Missing parameter content type');
	}
});

const port = 5008;
app.listen(port, () => {
	console.log(`Example app listening at http://localhost:${port}`);
});
