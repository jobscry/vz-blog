$(document).ready(function(){$('#comments h3').after('<p><strong><a href="#" id="toggle-comment-form">Add a comment.</a></strong></p>');$('#comment-form').slideToggle('medium');$('#toggle-comment-form').click(function(){$('#comment-form').slideToggle('medium');$(this).slideToggle('medium');return false;});$("input#id_honeypot").prev('label').andSelf().hide();$('#submit-button').parent().hide();var wait
$('#id_search_string').keyup(function(){clearTimeout(wait);wait=setTimeout("getPosts()",1000);});$.ajax({type:'GET',url:'http://twitter.com/statuses/user_timeline/jobscry.json',dataType:'jsonp',data:'count=3',success:function(tweets){$('#secondary > div.content').append('<div id="tweets"><h3>Tweets</h3></div>');$.each(tweets,function(i,tweet){$('#tweets').append('<p>'+tweet.text+'<br />'+prettyDate(tweet.created_at)+' via '+tweet.source+'</p>');})},})});function getPosts(){$.ajax({cache:false,dataType:'json',data:'search_string='+$('#id_search_string').val(),type:'GET',url:'/posts/search/',success:function(posts){$('#search-results').html('<p>Found '+posts.length+' post(s) with <em>'+$('#id_search_string').val()+'</em></p><ul class="results"></ul>');$.each(posts,function(i,post){$('ul.results').append('<li><a href="/posts/'+post.fields.slug+'">'+post.fields.title+'</a>, '+prettyDate(post.fields.published_on)+'</li>');});}})}
/*
 * JavaScript Pretty Date
 * Copyright (c) 2008 John Resig (jquery.com)
 * Licensed under the MIT license.
 */
function prettyDate(time){var date=new Date((time||"").replace(/-/g,"/").replace(/[TZ]/g," ")),diff=(((new Date()).getTime()-date.getTime())/1000),day_diff=Math.floor(diff/86400);if(isNaN(day_diff)||day_diff<0||day_diff>=31)return;return day_diff==0&&(diff<60&&"just now"||diff<120&&"1 minute ago"||diff<3600&&Math.floor(diff/60)+" minutes ago"||diff<7200&&"1 hour ago"||diff<86400&&Math.floor(diff/3600)+" hours ago")||day_diff==1&&"Yesterday"||day_diff<7&&day_diff+" days ago"||day_diff<31&&Math.ceil(day_diff/7)+" weeks ago";}