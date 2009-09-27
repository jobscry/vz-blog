$(document).ready(function () {
    $('#site_menu_toggle').addClass('jqueryied');
    $('div#site_menu').hide(500);
    $('#site_menu_toggle').click(function(){
        $('div#site_menu').slideToggle("slow", function(){
            $.scrollTo('#site_menu_toggle');
        });
    });
});
