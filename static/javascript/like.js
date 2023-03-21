function like(username, id) {
    var site = "/musicBlogger/"
    
    $.get(window.location.href.substring(0, window.location.href.indexOf(site) + site.length) + "like", {"username": username, "id":id}, 
    function(data){
        var point = '#like-' + id
        var button = $(point);
        if(data.results == 0){
            console.log("0")
            button.text('Like');
        }else if (data.results == 1){
            console.log("1")
            button.text('Liked');
        }else{
            alert("Error with liking song");
        }  
    })
}