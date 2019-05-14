$(document).ready( function () {
    $('#modalBuscarDependencias').on('shown.bs.modal', function () {
        $('#input_search').focus();
    });
    $('.btnSeleccionarDependencia').on("click", function() {
        var tipo = $(this).parents('td').siblings('.fila_tipo').html();
        var codigo = $(this).parents('td').siblings('.fila_codigo').html();
        var getUrl = window.location;
        var datos = {tipo: tipo, cod: codigo};
        $.ajax({
                method: 'POST',
                url: getUrl.origin+'/empleado/api/v1/dependencias',
                data: datos,
                success: function(data, status, xho){
                    cargarSelects(data.data);
                    $('#modalBuscarDependencias').modal('hide');
                },
                error: function(data){
                    console.log(data);
                }
        })
    });

    function cargarSelects(resultado){
        $('#id_circunscripcion').val(resultado['id_circunscripcion']);
        $('#id_unidad').val(resultado['id_unidad']);
        $('#id_organismo').val(resultado['id_organismo']);
        $('#id_dependencia').val(resultado['id_dependencia']);
        $('#id_direccion').val(resultado['id_direccion']);
        $('#id_departamento').val(resultado['id_departamento']);
        $('#id_division').val(resultado['id_division']);
    }

} );