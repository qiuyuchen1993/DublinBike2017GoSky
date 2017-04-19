var xmlhttp = new XMLHttpRequest();
var url = "myTutorials.txt"

xmlhttp.onreadystatechange = function(){
    if(this.readyState==4 && this.status ==200){
        var myArr = JSON.parse(this.responseText);
        myFunction(myArr);
    }
};
xmlhttp.open("GET",url,true);
xmlhttp.send();

function myFunction(arr){
    var out = " ";
    var i;
    for(i=0; i<arr.length; i++){
        out += '<a herf="' + arr[i].url + '">' +
        arr[i].display + '</a><br>';
    }
    document.getElementById("id01").innerHTML = out;
}

var jqxhr = $.getJSON("example.json",function()){
                      console.log("success");
                      })
                      .done(function()){
                            console.log("second success");
                            })
                      .fail(function(){
                          console.log("error");
                      })
                      .always(function(){
                          console.log("complete");
                      });

    /* 
      <script language="JavaScript" type="text/javascript" src="static/XMLHttpRequest.js"></script> */