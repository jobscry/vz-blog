$(document).ready(function () {
    $.ajax({
        beforeSend: function(){
            $('div.stream').append('<span id="ajax-spinner-container">&nbsp;<img id="ajax-spinner" src="/media/images/ajax-spinner.gif" height="16" width="16" alt="ajax request in progress"></span>');
        },
        dataType: 'json',
        type: 'GET',
        url: '/stream/json/',
        success: function(items){
            $.each(items, function(i, item){
               var elem = '<li class="stream stream_'+item.source.toLowerCase()+'">'+item.text+' <a href="'+item.url+'">#</a> - <span class="stream_published_on">'+prettyDate(item.created_on)+'</a></li>';
               if ($('ul.stream').length == 0){
                   $('div.stream').append('<ul class="stream">'+elem+'</ul>');
               } else {
                   $('ul.stream').append(elem);
               }
            });
           $('span#ajax-spinner-container').remove();
        }
    });
});
