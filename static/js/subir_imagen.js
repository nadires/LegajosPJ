$(function () {

  $(".js-upload-photos").click(function () {
    $("#fileupload").click();
  });

  $("#fileupload").fileupload({
    dataType: 'json',
    done: function (e, data) {
      console.log(data.result.mensaje);
      if (data.result.is_valid) {
        $("#gallery tbody").prepend(
          "<tr><td><img src='" + data.result.url + "' width='100px' height='80px'><a href='" + data.result.url + "'>" + data.result.name + "</a></td></tr>"
        )
      }
    }

  });

});