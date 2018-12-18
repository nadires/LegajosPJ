$(function () {

  $(".js-upload-photos").click(function () {
    $("#fileupload").click();
  });

  $("#fileupload").fileupload({
    dataType: 'json',
    done: function (e, data) {
      console.log(data.result.mensaje);
      if (data.result.is_valid) {
        $("#aniimated-thumbnials").prepend(
          "<div class='col-lg-3 col-md-4 col-sm-6 col-xs-12'>"+
              "<a href='" + data.result.url + "' data-sub-html='Legajo'>"+
                  "<img class='img-responsive thumbnail' src='" + data.result.url + "'>"+
              "</a>"+
          "</div>"
          )
        $("#cartel_imagenes_no_cargadas").hide();
      }
    }

  });

});