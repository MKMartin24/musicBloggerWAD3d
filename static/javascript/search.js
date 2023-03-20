function search() {
  var query = document.getElementById('search-input').value;
  $.get(window.location.href, {"query":query}, 
  function(data){
    $('#results').replaceWith(data);
  })

}

// function showResults(results_songs) {
//   var output = '';
//   if (results_songs.length > 0) {
//       output += '<div>';
//       for (var i = 0; i < results_songs.length; i++) {
//         output += '<div class="song">';
//         output += '<h3>' + results_songs[i].name + '</h3>';
//         output += '<img src="' + results_songs[i].image + '">';
//         output += '<p>' + results_songs[i].text + '</p>';
//         output += '</div>';
//       }
//       output += '</div>';
//   } else {
//       output += 'No results found.';
//   }
//   document.getElementById('results_songs').innerHTML = output;
// }