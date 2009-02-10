$(document).ready(function () {
    $('#submit-button').parent().hide();
    var wait;
    $('#id_search_string').keyup(
        function(){
            clearTimeout(wait);
            wait = setTimeout("getPosts()", 1000);
        }
    );
});
function getPosts(){
    $.ajax({
        beforeSend: function(){
            $('#id_search_string').after('<span id="ajax-spinner-container">&nbsp;<img id="ajax-spinner" src="/media/images/ajax-spinner.gif" height="16" width="16" alt="ajax request in progress"></span>');
        },
        cache: false,
        dataType: 'json',
        data: 'search_string='+$('#id_search_string').val(),
        type: 'GET',
        url: '/posts/search/',
        success: function(posts){
            $('#search-results').html('<p>Found '+posts.length+' post(s) with <em>'+$('#id_search_string').val()+'</em></p><ul class="results"></ul>');
            $.each(posts, function(i, post){
                $('ul.results').append('<li><a href="/posts/'+post.fields.slug+'">'+post.fields.title+'</a>, '+prettyDate(post.fields.published_on)+'</li>');
            });
            $('span#ajax-spinner-container').remove();
        }
    });
}
