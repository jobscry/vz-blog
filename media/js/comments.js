$(document).ready(function () {
    $('#comments h3').after('<p><strong><a href="#" id="toggle-comment-form">Add a comment.</a></strong></p>');
    $('#comment-form').slideToggle('medium');
    $('#toggle-comment-form').click(
        function(){
            $('#comment-form').slideToggle('medium');
            $(this).slideToggle('medium');
            return false;
        }
    );
    $("input#id_honeypot").prev('label').andSelf().hide();
});
