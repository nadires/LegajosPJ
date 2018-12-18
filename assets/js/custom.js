$(function () {
  alert("sdfgsdf");
  $('select').on('select2:select', function (event) {
  console.log(event.params.data.id);
  });

});