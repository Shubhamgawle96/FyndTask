//open add movie modal
function add_movie(){

//   var modal = document.getElementById("myModal");
   modal = document.getElementById("myModal");
   modal.style.display = "block";

}

//open edit modal
function edit_movie(){
   $.get('/movie',function(response, status){
            resp = JSON.parse(response);
            console.log("movie name",resp);

              var ele = document.getElementById('mnamechng');
                for (var i = 0; i < resp.length; i++) {
                    // POPULATE SELECT ELEMENT WITH JSON.
                    ele.innerHTML = ele.innerHTML +
                        '<option value="' + resp[i] + '">' +resp[i] + '</option>';
                }

            modal = document.getElementById("myModaledit");
            modal.style.display = "block";
})}

//open del modal
function del_movie(){
    $.get('/movie',function(response, status){
            resp = JSON.parse(response);
            console.log("movie name",resp);

              var ele = document.getElementById('mnamedel');
                for (var i = 0; i < resp.length; i++) {
                    // POPULATE SELECT ELEMENT WITH JSON.
                    ele.innerHTML = ele.innerHTML +
                        '<option value="' + resp[i] + '">' +resp[i] + '</option>';
                }

            modal = document.getElementById("myModaldel");
            modal.style.display = "block";
})
}

//for closing modal
function close_me(value){
    document.getElementById(value).style.display = 'none';
}

//to add movie to db
function add_db(){
    form = document.getElementById("add_form");
    var i;
    var count = 0;
    for(i=0;i<form.length;i++){
        if(form.elements[i].value != ''){
            count++
        };

    }
    if(count == 5){
          var x = document.getElementById("add_form");
          var i;
          var dict = new Object();
          for (i = 0; i < x.length-1; i++) {
            console.log(x.elements[i]);
            console.log(x.elements[i].name,"haha",x.elements[i].value);
            dict[x.elements[i].name] = x.elements[i].value;
          }
        console.log("This is the dict",dict);

        $.post('/add',dict, function(response, status){
                console.log("Successfully posted");
                close_me('myModal');
                location.reload();
          });



    }
    else{
        alert("All fields are compulsary");
    }

}

//To edit movie
function edit_db(){
    console.log("This is the edit function");
    form_data_dict = {};
    form = document.getElementById("edit_form");
    var movie_name = document.getElementById("mnamechng");
    if(movie_name.value == ''){
        alert("Movie name to change cannot be empty");
    }
    else{
    for(i=0;i<form.length;i++){
        var field_name  = form.elements[i].name;
        var field_value = form.elements[i].value;
        form_data_dict[field_name] = field_value;
    }
    console.log("form edkited data dict",form_data_dict) ;
     $.post('/edit',form_data_dict, function(response, status){
        console.log("Successfully posted");
        close_me('myModaledit');
        location.reload();
     });
     }

}

//to delete movie
function del_db(){
    var movie_name = document.getElementById("mnamedel").value;
    if(movie_name.value == ''){
        alert("Movie name to delete cannot be empty");
    }
    else{
        var form_data_dict = {}
        form_data_dict['movie_name'] = movie_name;
        console.log("del dict",form_data_dict)
       $.post('/delete',form_data_dict, function(response, status){
            console.log("Successfully posted");
            close_me('myModaldel');
            location.reload();
       })
    }
}

//to open search result modal
function open_search_modal(resp){
    console.log("in open_search_modal",resp);
    if(resp['notfound'] == 'notfound'){
        alert("Movie not found");
    }
    else{
        var table = document.getElementById("search_table");

        console.log("search_table",table);
        $('#search_table').empty();
        $('#search_table').append('<tr><th>Name</th><th>Score</th><th>Director</th><th>Popularity</th><th>Genre</th></tr>');
        $('#search_table').append('<tr id="search_row"></tr>');
        var row = document.getElementById("search_row");
        console.log("tavleeee",$('#search_table'))
        console.log("search_roe",row);
        row.innerHTML = row.innerHTML + '<td>' + resp['name'] + '</td>' + '<td>' + resp['score'] + '</td>' +
         '<td>' + resp['director'] + '</td>' +'<td>' + resp['popularity'] + '</td>' +'<td>' + resp['genre'] + '</td>';
        search_modal = document.getElementById("searchmodal");
        search_modal.style.display = 'block';
    }


}


//funciton to search movie
function search_movie(){
    var movie_name = document.getElementById("search").value;
    if(movie_name == ''){
        alert('movie name cannot be empty');
    }
    else{
        var form_data_dict = {}
        form_data_dict['movie_name'] = movie_name;
        $.post('/search',form_data_dict, function(response, status){
            resp = JSON.parse(response);
            console.log("search_resp",resp);
            open_search_modal(resp);
       })
    }

}
