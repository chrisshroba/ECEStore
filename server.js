var http =		require("http");
var url  = 		require("url");
var querystring = 	require("querystring");
var mustache = 		require("mustache");
var fs =		require("fs");


var port = 8001;

var server = http.createServer(function(req,res) {

var pathname = url.parse(req.url).pathname;
var query = querystring.parse(url.parse(req.url).query);

route(req,res,pathname,query);



});

function route(req,res,pathname,query)
{
	if(pathname in handle)
	{
		handle[pathname](req,res,pathname,query);
	}
	else
	{
		handle["/404"](req,res,pathname,query);
	}
	
}

function searchPage(req,res,pathname,query)
{

	console.log("Search")

	searchResults = {results:[
	{barcode:"123456",part_number:"DXZ_ 123",description:"Legos",manufacturer:"Legos Inc.",price:"0.99"},

	{barcode:"123456",part_number:"DXZ_ 123",description:"Legos",manufacturer:"Legos Inc.",price:"0.99"},
	
	{barcode:"123456",part_number:"DXZ_ 123",description:"Legos",manufacturer:"Legos Inc.",price:"0.99"},

	{barcode:"123456",part_number:"DXZ_ 123",description:"Legos",manufacturer:"Legos Inc.",price:"0.99"},
	
	{barcode:"123456",part_number:"DXZ_ 123",description:"Legos",manufacturer:"Legos Inc.",price:"0.99"},

	{barcode:"123456",part_number:"DXZ_ 123",description:"Legos",manufacturer:"Legos Inc.",price:"0.99"}
	


				]};
	w(2);
	res.writeHead(200,{"content-type": "text/html"});
	w(3);
	var bodyTemplate = readFile("results.template");
	w(4);
	var docTemplate  = readFile("document.template");
	w(5);
	var docTitle =  "Search Results";
	w(6);
	var docBody  = 	mustache.render(bodyTemplate,searchResults);
	w(7);
	var doc = 	mustache.render(docTemplate,{title: docTitle, body: docBody});
	w(8);
	
	
	res.write(doc);
	res.end();


}

function e404Page(req,res,pathname,query)
{
	res.end("File not found");



}

function readFile(path)
{
	return fs.readFileSync(path).toString();
}

handle={};

handle["/search"] = searchPage;

handle["/404"] = e404Page;



server.listen(port);



function w(s){console.log(s);}
