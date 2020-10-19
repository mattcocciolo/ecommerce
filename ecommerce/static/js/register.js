/* Este javascript oculta o muestra el password */

    $(document).ready(function() {
    $("#show_hide_password1 span").on('click', function(event) {
        event.preventDefault();
        if($('#show_hide_password1 input').attr("type") == "text"){
            $('#show_hide_password1 input').attr('type', 'password');
            $('#show_hide_password1 span').addClass( "fa-eye" );
            $('#show_hide_password1 span').removeClass( "fa-eye-slash" );
        }else if($('#show_hide_password1 input').attr("type") == "password"){
            $('#show_hide_password1 input').attr('type', 'text');
            $('#show_hide_password1 span').removeClass( "fa-eye" );
            $('#show_hide_password1 span').addClass( "fa-eye-slash" );
        }
    });
});

$(document).ready(function() {
    $("#show_hide_password2 span").on('click', function(event) {
        event.preventDefault();
        if($('#show_hide_password2 input').attr("type") == "text"){
            $('#show_hide_password2 input').attr('type', 'password');
            $('#show_hide_password2 span').addClass( "fa-eye" );
            $('#show_hide_password2 span').removeClass( "fa-eye-slash" );
        }else if($('#show_hide_password2 input').attr("type") == "password"){
            $('#show_hide_password2 input').attr('type', 'text');
            $('#show_hide_password2 span').removeClass( "fa-eye" );
            $('#show_hide_password2 span').addClass( "fa-eye-slash" );
        }
    });
});