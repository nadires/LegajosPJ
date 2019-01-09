$(document).ready(function() {

	var endpoint = 'http://127.0.0.1:8000/empleados/api/v1/readonly-viewset/';

	function getListadoEmpleados(texto){
		$.ajax({
			method: 'GET',
			url: endpoint+'?search='+texto,
			success: function(data, status, xho){
				llenarHTML(data);
			},
			error: function(data){
				console.log("Error!");
				console.log(data);
			}
		});
	};

	
	$('#search').keypress(function(e){
		if(e.which == 13) {				// Al presionar Enter llama al método para obtener el listado
        	getListadoEmpleados($(this).val());
    	}
	});


	function llenarHTML(datos){
		for (var i = 0; i < datos.length; i++) {
			$('#cuerpo_tabla').append(
			"<tr>"+
                    "<td><a href='{% url 'empleado_detail' "+datos[i].id+" %}''>"+datos[i].apellido+", "+datos[i].nombre+"</a></td>"+
                    "<td>"+datos[i].legajo+"</td>"+
                    "<td>"+datos[i].cuil+"</td>"+
                    "<td>"+datos[i].dni+"</td>"+
                  "</tr>"
            );
		}
	};


});