/*$(function () {*/
  /*var select = $('#id_familiares');
  console.log(select);
  var lista = select.find('ul');
  console.log(lista);
  console.log(lista.length);
  console.log($('.select2-selection__rendered'));
  lista.on('change', function (event) {
  console.log(event.target);
  });*/
  /*console.log($('ul')[1]);*/
  /*$('select[name="familiares"]').on('change', function(event) {
  console.log(event.target);
});*/

/*});*/
/*$(document).on('autocompleteLightInitialize', '[data-autocomplete-light-function=select2]', function() {
    // do select2 configuration on $(this)
    $(this).select2(console.log("hace algoo"));
    console.log($(this));
  });

/*(function($){
    $(document).on('autocompleteLightInitialize', '[data-autocomplete-light-function=select2]',
      function () {
        console.log("sds");
        $(this).on('select2:selecting', function (evt) {
          console.log('wheee', evt);
        });
      }
    );
})(yl.jQuery);*/
document.querySelector('select[name="familiares"]').onchange=function(event) {
  var listado = event.target.nextSibling.getElementsByClassName("select2-selection__choice");
  for(var i=0; i<listado.length; i++){
    /*listado[i].setAttribute("hidden", true);*/
    listado[i].style.visibility = "hidden";
    console.log(listado[i]);
  }
  /*console.log(listado);*/
  var tableRef = document.getElementById('cuerpo_tabla');

  // Insert a row in the table at the last row
  var newRow   = tableRef.insertRow(tableRef.rows.length);

  // Insert a cell in the row at index 0
  var newCell  = newRow.insertCell(0);

  // Append a text node to the cell
  var newText  = document.createTextNode('Nombre de la persona');
  
  newCell.appendChild(newText);
  newCell  = newRow.insertCell(1);
  newText  = document.createTextNode('Parentesco');
  newCell.appendChild(newText);
};