function search() {
  var query = document.getElementById('search-input').value;
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
      var results_songs = JSON.parse(xhr.responseText);
      showResults(results_songs); 
    }
  };
  xhr.open('GET', '/search?q=' + query);
  xhr.send();
}

function showResults(results_songs) {
  var output = '';
  if (results_songs.length > 0) {
      output += '<div>';
      for (var i = 0; i < results_songs.length; i++) {
        output += '<div class="song">';
        output += '<h3>' + results_songs[i].name + '</h3>';
        output += '<img src="' + results_songs[i].image + '">';
        output += '<p>' + results_songs[i].text + '</p>';
        output += '</div>';
      }
      output += '</div>';
  } else {
      output += 'No results found.';
  }
  document.getElementById('results_songs').innerHTML = output;
}