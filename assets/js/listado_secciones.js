$(document).ready(function() {
    var url_data = window.location.origin;
    var id_persona = window.location.pathname.split('/')[3];

    $.ajax({
            method: 'GET',
            url: url_data + '/legajos/' +id_persona,
            success: function(data, status, xho){
                console.log(status);
            },
            error: function(data){
                console.log(status);
            }
        })

    $("#simplePrint").click(function(){

                $('#toPrint').printElement();
           });

});