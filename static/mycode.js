console.log('ayy js');

var movieNo=0;
var movieNo2=0;
var currentMovie;

var switchMovie = function switchMovie() {
    console.log('switchMovie');
    $.get('/iterate', function(e) {
	console.log('iteratin');
	console.log(movieNo);
	$('#shows').text('');
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
	if(movieNo == movieInfo.length){
	    movieNo = 0;
	}
	console.log(movieNo);
	currentMovie=movieInfo[movieNo];
    });
};

/*var switchMovie2 = function switchMovie2() {
    console.log('switchMovie2');
    $.get('/recommend', function(e) {
	console.log('recommendin');
	console.log(movieNo2);
	$('#shows').text('');
	movieInfo=JSON.parse(e);
	//currentMovie=movieInfo;
	console.log('did cM thing');
	console.log(movieInfo);
	console.log('just printed');
	var name=movieInfo[movieNo2]['name'];
	console.log(name);
	var poster=movieInfo[movieNo2]['poster'];
	var blurb=movieInfo[movieNo2]['blurb'];

	$('#movieName').text(name);
	$('#blurb').text(blurb);
	$('#poster').attr('src', poster);
	movieNo2++;
	if(movieNo2 == movieInfo.length){
	    movieNo2 = 0;
	}
	console.log(movieNo2);
	currentMovie=movieInfo[movieNo2];
    });
};*/

var chooseMovie = function chooseMovie() {
    console.log('chooseMovie');
    $.ajax({
	url: '/find_tix',
	data: currentMovie,
	type: 'POST',
	success: function(e) {
	    var showtimeData=JSON.parse(e);
	    console.log(showtimeData);
	    console.log(showtimeData.length);
	    //console.log(showtimeData[0][0]['avail']);
	    var showtimes=[];
	    for ( i=0; i<showtimeData.length; i++) {
		console.log('in loop1');
		$('#shows').append('<h2>');
		$('#shows').append(showtimeData[i][0]['theatreName']);
		$('#shows').append('</h2>');
		$('#shows').append('<h3>');
		$('#shows').append(showtimeData[i][0]['address']);
		$('#shows').append('</h3><br> <div class="container">');
		for (j=0; j<showtimeData[i].length; j++) {
		    console.log('in loop2');
		    console.log(showtimeData[i][j]['avail']);
		   
		    var n=showtimeData[i][j]['avail'].localeCompare('false');
		    console.log(n);
		    if (showtimeData[i][j]['avail'].localeCompare('False')==0) {
			console.log('same');
			$('#shows').append('<a href="');
			$('#shows').append('    '+showtimeData[i][j]['buy']);
		    }
		    $('#shows').append('" class="btn btn-info" role="button">');
		    $('#shows').append(showtimeData[i][j]['time']);
		    $('#shows').append('</a>');

		    $('#shows').append('<br>');
		    //$('#shows').append(showtimeData[i][j]['avail']);
		}
		$('#shows').append('</div><br>');
		
	    }
	    //console.log(showtimes[0]['avail']);
	    //console.log(document.getElementById('shows'));
	    //document.getElementById('shows').innerHTML='ayy';
	    
	    },
	error: function(error) {
	    console.log(error);
	}
    });
};

switchMovie();
document.getElementById("switch").addEventListener("click", switchMovie);
document.getElementById("watch").addEventListener("click", chooseMovie);
//document.getElementById("switch2").addEventListener("click", switchMovie2);
console.log("stuff")
