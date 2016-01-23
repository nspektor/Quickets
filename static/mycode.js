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
    $.ajax({
	url: '/find_tix',
	data: currentMovie,
	type: 'POST',
	success: function(e) {
	    var showtimeData=JSON.parse(e);
	    console.log(showtimeData);
	    console.log(showtimeData[0][0]);
	    var showtimes=[];
	    for ( i=0; i<showtimeData[0].length; i++) {
		showtimes.push(showtimeData[0][i]);
	    }
	    console.log(showtimes[0]['avail']);
	},
	error: function(error) {
	    console.log(error);
	}
    });
};
    
document.getElementById("switch").addEventListener("click", switchMovie);
document.getElementById("watch").addEventListener("click", chooseMovie);
