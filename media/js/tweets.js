$(document).ready(function () {
	$.ajax({
		type: 'GET',		
		url: 'http://twitter.com/statuses/user_timeline/jobscry.json',
		dataType: 'jsonp',
		data: 'count=3',
		success: function(tweets){	
			$.each(tweets, function(i, tweet){
				$('#tweets').append('<p>'+tweet.text+'<br />'+prettyDate(tweet.created_at)+' via '+tweet.source+'</p>');
			})
		},
	})
});
