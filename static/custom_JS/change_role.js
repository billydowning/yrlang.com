
 $(document).ready(function(){


  $("#clientButton").click(function(){
       $.get("/users/change-as-provider", function( status, data){

            window.location.href = "/"
      });

    });

   $("#providerButton").click(function(){
     $.get("/users/change-as-client", function( status, data){

            window.location.href = "/"
      });


         });
});
