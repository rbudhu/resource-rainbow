$(document).ready(function() {
    $('.submit').click(function() {
        var $form = $(this).closest('form');
        var user = $('[name=user_id]', $form).val();
        var data = $form.serialize();
        $.post(urls.workgroup_user_remove(), data, 
               function(response) {
                   console.log(response);
                   $('#person-'+user).fadeOut(2000);
                   
               });
        
    });
});
