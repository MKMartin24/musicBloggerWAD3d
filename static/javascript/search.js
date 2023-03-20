function search() {
  var query = document.getElementById('search-input').value;
  $.get(window.location.href, {"query":query}, 
  function(data){
    $('#results').replaceWith(data);
  })
}