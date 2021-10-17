$('#sub').click(function (e) {
    var username = $("input#username").val();
    var password = $("input#password").val(); 

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