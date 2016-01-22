console.log('ayy js');

var movieNo=0;
var currentMovie;

var switchMovie = function switchMovie() {
    console.log('switchMovie');
    $.get('/iterate', function(e) {
	console.log('iteratin');
	console.log(movieNo);
	movieInfo=JSON.parse(e);
	//currentMovie=movieInfo;
	console.log('did cM thing');
	console.log(movieInfo);
	console.log('just printed');
	var name=movieInfo[movieNo]['name'];
	console.log(name);
	var poster=movieInfo[movieNo]['poster'];
	var blurb=movieInfo[movieNo]['blurb'];

	$('#movieName').text(name);
	$('#blurb').text(blurb);
	$('#poster').attr('src', poster);
	movieNo++;
	console.log(movieNo);
	currentMovie=movieInfo[movieNo];
    });
};

var chooseMovie = function chooseMovie() {
    console.log('chooseMovie');
    var data={currentMovie};
    $.post('/find_tix', currentMovie);
    console.log('fin choose');
};
    
document.getElementById("switch").addEventListener("click", switchMovie);
document.getElementById("watch").addEventListener("click", chooseMovie);
