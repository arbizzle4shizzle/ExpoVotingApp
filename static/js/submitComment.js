// var mysql = require('mysql');

// var con = mysql.createConnection({
//   host: 'sql9.freemysqlhosting.net',
//   user: 'sql9219692',
//   password: '5M2YS1HZdZ',
//   database: 'sql9219692'
// });



// function submit_comment(teamNum) {
//     // """submits comment"""
//     console.log("submitted_comment")
//     textid = "textarea".concat(teamNum)
//     text = $("#textid").val()
//     try {
//         // get_cursor().execute("INSERT INTO Comment (TeamNum, TimeStamp, Text) VALUES (teamNum, Date.now(), text))
//         con.connect(function(err) {
//           if (err) throw err;
//           console.log("Connected!");
//           //Insert a record in the "customers" table:
//           var sql = "INSERT INTO Comment (TeamNum, TimeStamp, Text) VALUES (teamNum, Date.now(), text)";
//           con.query(sql, function (err, result) {
//             if (err) throw err;
//             console.log("1 comment inserted");
//           });
//         });
//     }  catch(error) {
//        console.log('error: '.concat(error))
//     }
// }