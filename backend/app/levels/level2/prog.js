con = require('@americanexpress/css-to-js');
con = con.convert;

let first = `
.header {
    width: 800px;
    height: 50px;
    color: blue;
  }
  
  .main-table {
    width: 900px;
    height: 1100px;
    color: blue;
  }
  
  .footer {
    width: 800px;
    height: 40px;
    color: blue;
  }
`;

let second = `
.header {
    width: 800px;
    height: 50px;
    color: red;
  }
  
  .main-table {
    width: 900px;
    height: 1100px;
    color: red;
  }
  
  .footer {
    width: 800px;
    height: 40px;
    color: red;
  }
`;

console.log(process.argv[0])

// var fs = require("fs");
// = fs.readFileSync("./mytext.txt");
// let third = ;


const checkIfGood = (firstVersion, secondVersion, submittedVersion) => {
  let firstConv = convert(firstVersion);
  let secondConv = convert(secondVersion);
  let thirdConv = convert(submittedVersion);
  if (
    firstConv?.header?.color === thirdConv?.header?.color &&
    firstConv['main-table']?.color === thirdConv['main-table']?.color &&
    firstConv?.footer?.color === thirdConv?.footer?.color
  ) {
    return true;
  }

  if (
    secondConv.header?.color === thirdConv?.header?.color &&
    secondConv['main-table']?.color === thirdConv['main-table']?.color &&
    secondConv.footer?.color === thirdConv?.footer?.color
  ) {
    return true;
  }
};