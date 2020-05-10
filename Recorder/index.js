const cv = require('opencv4nodejs');
const express = require("express");
const app = express() ;
const path = require("path");
const server = require('http').Server(app);
const io = require('socket.io')(server);
var fs = require('fs');
var shell = require('shelljs');

const querystring = require('querystring');



var bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended : false} ));


/*app.get('/training' , function (req,res) { 
	shell.exec('bash movefile.sh')

});*/






app.post('/submit-label', function (req,res) {
	var action = "custom_images/" + req.body.actionName + "_";
	const query = querystring.stringify({"actionName" : action});
	fs.mkdirSync(action);
	console.log("CREATE DIRECTORY " + action);
	res.redirect('/recorder?' + query);
	
	
});


app.get('/', (req,res) => {
	console.log("CAME TO HOME");
	var dir = "./custom_images"
	if (!fs.existsSync(dir)){
		fs.mkdirSync(dir);
	}
	console.log("Created Directory custom_images")
	res.sendFile(path.join(__dirname, 'form.html'));
});





//const wCap = new cv.VideoCapture(0);

app.get('/recorder', (req,res) => {
	i = 0 

	const wCap = new cv.VideoCapture(0);
	wCap.set(cv.CAP_PROP_FRAME_WIDTH,640);
	wCap.set(cv.CAP_PROP_FRAME_HEIGHT, 480); 

	res.sendFile(path.join(__dirname, 'index.html'));







var INTER = setInterval(() => {
	
	const frame = wCap.read();
	i = i + 1
	

	try{
	var action = req.query.actionName;
	var j = ('00000'+i).slice(-5)
	console.log(action)
	cv.imwrite(action + "/" + j + '.jpg',frame);
		
	console.log("FRAME WAS WRITTEN");
	const image = cv.imencode('.jpg', frame).toString('base64');
	io.emit('image', image);
	if(i == 300){
		i = 0;
		wCap.release();
		console.log("RECORDED 300 FRAMES, STOPPED RECORDING NOW");
		clearInterval(INTER);
		
	}

	}
	catch (e){
		console.log(e);
	}



},1000/30)




});


console.log("LISTENING ON PORT 5001")
server.listen(80);
