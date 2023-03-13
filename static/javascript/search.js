function search() {
    var query = document.getElementById('search-input').value;
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        var data = JSON.parse(xhr.responseText);
        showResults(data.results_songs, "songs"); 
        showResults(data.results_profiles, "profiles");
        showResults(data.results_blogs, "blogs");
      }
    };
    xhr.open('GET', '/search?q=' + query);
    xhr.send();
  }

function showResults(results, type) {
    var output = '';
    if (results.length > 0) {
        output += '<ul>';
        for (var i = 0; i < results.length; i++) {
            output += '<li>' + results[i].field1 + ' - ' + results[i].field2 + '</li>';
        }
        output += '</ul>';
    } else {
        output += 'No results found.';
    }
    document.getElementById('search-results').innerHTML = output;
}