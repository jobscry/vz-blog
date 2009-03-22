$(document).ready(function () {
    $.ajax({
        beforeSend: function(){
            $('div.stream > .content').after('<span id="ajax-spinner-container">&nbsp;<img id="ajax-spinner" src="/media/images/ajax-spinner.gif" height="16" width="16" alt="ajax request in progress"></span>');
        },
        cache: false,
        dataType: 'json',
        type: 'GET',
        url: '/stream/ajax/',
        success: function(items){
            $.each(items, function(i, item){
               var elem = '<li class="stream_'+item.feed.toLowerCase()+'">'+item.title+' [<a href="'+item.link+'" title="link">#</a>]<span class="stream_published_on">'+prettyDate(item.published_on)+'</span></li>';
               if ($('ul.stream').length == 0){
                   $('div.stream > .content').append('<ul class="stream">'+elem+'</ul>');
               } else {
                   $('ul.stream').append(elem);
               }
            });
           $('span#ajax-spinner-container').remove();
        }
    });
});
