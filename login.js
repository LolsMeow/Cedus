$('#sub').click(function (e) {
    var username = $.trim$("input#username").val();
    var password = $.trim$("input#password").val(); 

    $.ajax({
        url : "{% 'login' %}",
        type : 'POST',
        data : {
            'username' : username,
            'password' : password
        },
        dataType : 'json',
        success : function (data) {
            if (data != null && data.success == true) {
                window.location = '/'
            }
            else {
                $('#sub').append(data);
                alert(data);
            }

        }
    })
});