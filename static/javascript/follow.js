function follow(id) {
    $.get(window.location.href+"follow", { "id":id}, 
    function(data){
        var button = $('#follow-button');
        if(data.results == 0){
            button.text('Following');
        }else if (data.results == 1){
            button.text('Follow');
        }else{
            alert("Error with follow button");
        }  
    })
}