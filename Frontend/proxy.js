const fs = require('fs');

// read/process package.json
const file = './package.json';
// console.log(JSON.parse(fs.readFileSync(file).toString()));
let pkg = JSON.parse(fs.readFileSync(file).toString());

// at this point you should have access to your ENV vars
pkg.proxy = `https://trading-system-workshop.herokuapp.com/`;

// console.log(pkg);
// the 2 enables pretty-printing and defines the number of spaces to use
fs.writeFileSync(file, JSON.stringify(pkg, null, 4));
