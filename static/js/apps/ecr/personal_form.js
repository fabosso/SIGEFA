$('#hidden-spinner').hide();


$('.add-personal-button').on('click', function(e){
   e.preventDefault()
   // Frontend dinamics
   $('.add-personal-button').hide();
   $('#hidden-spinner').show();
   
   // Collect form data
   parameters = new FormData(document.getElementById("PersonalForm"))

   // Ajax to send data
   $.ajax({
      url: window.location.href,
      headers: {
         "X-CSRFToken": csrftoken,
       },
      data: parameters,
      method: 'POST',
      dataType: 'json',
      cache: false,
      processData: false,
      contentType: false,
   }).done(function(data){
      if (data.status == 200){
         $('#PersonalForm').trigger("reset");
         $("#hidden-spinner").hide();
         $('.add-personal-button').show();
         $('#PersonalTable tbody').html(data.html_personal_list)

         Swal.fire({
            position: 'center',
            icon: 'success',
            title: data['message'],
            showConfirmButton: false,
            timer: 3000
        })

      } else if (data.status == 400){
         errors = JSON.parse(data.errors)
         $("#hidden-spinner").hide();
         $('.add-personal-button').show();
         if ($("input").next('p').length) $("input").nextAll('p').empty();
         if ($("select").next('p').length) $("select").nextAll('p').empty();
            for (var name in errors){
               for (var i in errors[name]){
                  var $input = $('input[name='+name+']');
                  var $select = $('select[name='+name+']');
                  $input.after("<p style='color: #ff5f5fde;'>"+ errors[name][i].message+ "</p>");
                  $select.after("<p style='color: #ff5f5fde;'>"+ errors[name][i].message+ "</p>");
               }
            }
      } else if (data.status == 500){ 
         console.log(data)
      }
      
   }).fail(function (jqXHR, textStatus, errorThrown) {
      alert(textStatus + ': ' + errorThrown);
   }).always(function(data) {
   });

});