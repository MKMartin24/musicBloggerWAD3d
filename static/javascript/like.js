function like(username, id) {
    $.get(window.location.href+"like", {"username": username, "id":id}, 
    function(data){
        console.log(data.results)
        var button = $('#follow-button');
        if(data.results == 0){
            button.text('following');
        }else if (data.results == 1){
            button.text('follow');
        }else{
            alert("Error with follow button");
        }  
    })
}