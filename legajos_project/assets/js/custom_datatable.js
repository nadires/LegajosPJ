$(document).ready( function () {
    $('#listTable').DataTable({
        paging: false,      // Oculto la paginacion
        "bInfo" : false,     // Oculto el "Showing 1 of N entries"
        "language": {
          "emptyTable": "No hay elementos en la tabla",
          "zeroRecords": "No hay resultados en la búsqueda"
        }
    });

    // Defino que el input search es el creado manualmente
    var oTable = $('#listTable').DataTable();
    $("#input_search").on("keyup search input paste cut", function() {
        oTable.search($(this).val()).draw() ;
    });

    // Oculto el input search que viene por defecto
    $('#listTable_filter').parent().parent().hide();

} );