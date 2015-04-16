$(document).ready(function() {
    $('.submit').click(function() {
        var $btn = $(this);
        var $form = $(this).closest('form');
        var data = $form.serialize();
        $.post(urls.workgroup_user_add(), data,
               function(response) {
                   $btn.animate({'backgroundColor': '#5cb85c'}, 500,
                                function() {
                                    $btn.animate({'backgroundColor': 'white'}, 500);
                                });
               });
    });
});
