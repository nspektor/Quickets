console.log('ayy js');

var movieNo=0;
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
		$('#shows').append('</h3><br> <div class="containter">');
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
		//showtimes.push(showtimeData[i]);
		//console.log(showtimes[i]);
		//$('#shows').append(showtimes[i]['avail']);
		//$('#shows').append(showtimes[i]['theatreName']);
		//$('#shows').append(showtimes[i]['time']);
		//$('#shows').text(showtimes[i]['avail']);
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
