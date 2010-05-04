$(document).ready(function () {
    $.ajax({
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
        }
    });
});
