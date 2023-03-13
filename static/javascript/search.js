function search() {
    var query = document.getElementById('search-input').value;
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        var data = JSON.parse(xhr.responseText);
        showResults(data.results_songs, "cover_images"); 
        showResults(data.results_profiles, "profile_images");
        showResults(data.results_blogs, "blog_images");
      }
    };
    xhr.open('GET', '/search?q=' + query);
    xhr.send();
  }

function showResults(results, type) {
    var output = '';
    if (results.length > 0) {
        output += '<div>';
        for (var i = 0; i < results.length; i++) {
          template(name, type+"/"+image, text);
        }
        output += '</div>';
    } else {
        output += 'No results found.';
    }
    document.getElementById('type').innerHTML = output;
}
function template(name, image, text) {
    return '<div class = "profile"><h3>' + name + 
    '</h3> <img src="' +
    image + '"><p>' +
    text + '</p></div>';
}