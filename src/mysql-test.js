var mysql = require('mysql');
 
var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  password : '1111',
  database : 'ytg'
});

connection.connect();
  
connection.query('select * from comment', function (error, results, fields) {
    if (error) {
        console.log(error);
    }
    console.log(results);
});
  
connection.end();