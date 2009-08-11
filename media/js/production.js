/*
 * JavaScript Pretty Date
 * Copyright (c) 2008 John Resig (jquery.com)
 * Licensed under the MIT license.
 */
// Takes an ISO time and returns a string representing how
// long ago the date represents.
function prettyDate(time){var date=new Date((time||"").replace(/-/g,"/").replace(/[TZ]/g," ")),diff=(((new Date()).getTime()-date.getTime())/1000),day_diff=Math.floor(diff/86400);if(isNaN(day_diff)||day_diff<0||day_diff>=31)return;return day_diff==0&&(diff<60&&"just now"||diff<120&&"1 minute ago"||diff<3600&&Math.floor(diff/60)+" minutes ago"||diff<7200&&"1 hour ago"||diff<86400&&Math.floor(diff/3600)+" hours ago")||day_diff==1&&"Yesterday"||day_diff<7&&day_diff+" days ago"||day_diff<31&&Math.ceil(day_diff/7)+" weeks ago";}
$(document).ready(function(){$('#submit-button').parent().hide();var wait;$('#id_search_string').keyup(function(){clearTimeout(wait);wait=setTimeout("getPosts()",1000)})});function getPosts(){$.ajax({beforeSend:function(){$('#id_search_string').after('<span id="ajax-spinner-container">&nbsp;<img id="ajax-spinner" src="/media/images/ajax-spinner.gif" height="16" width="16" alt="ajax request in progress"></span>')},cache:false,dataType:'json',data:'search_string='+$('#id_search_string').val(),type:'GET',url:'/posts/search/',success:function(posts){$('#search-results').html('<p>Found '+posts.length+' post(s) with <em>'+$('#id_search_string').val()+'</em></p><ul class="results"></ul>');$.each(posts,function(i,post){$('ul.results').append('<li><a href="/posts/'+post.fields.slug+'">'+post.fields.title+'</a>, '+prettyDate(post.fields.published_on)+'</li>')});$('span#ajax-spinner-container').remove()}})}
