$(document).ready(function() {
    $('.status-create').click(function() {
        var status_id = $(this).data('status-id');
        var user_id = $(this).data('user-id');
        $.post(urls.status_create(), {
            'status-id': status_id,
            'user-id': user_id
        }, function(data) {
            var $msg = $('#status-message');
            $('.alert > h4', $msg).html(data.message);
            $msg.show();
        });
    });

}); //end document ready
