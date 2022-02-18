var id_facilidad = $('#id_facilidad').text()


function create_sensor_card(data){
   card = `<div class="row justify-content-center text-center">`
   card += `<div class="col-md-6 mb-3">`
   card += `<h4>${data.nombre}</h4>`
   card += `<p>${data.indicador}</p>`
   card += `</div></div>`

   return card
}



if (sensor_created == 'True'){
      var scheme = window.location.protocol
      var path = scheme + '//' + window.location.host + '/';
      url = path + `api/facilidad/${id_facilidad}/sensor/${sensor_id}/edit/`


      var skeleton_form = $('.clone').clone(true);
      $('.card-body-form').html("")
      $('.card-body-form').append(skeleton_form)
      skeleton_form.removeClass('d-none')

      $.ajax({
         url: url,
         method: 'GET',
      }).done(function(data){
         console.log(data)
         $('.card-body-form').html("")
         card = create_sensor_card(data)
         $('.card-body-form').append(card)
         
      }).fail(function (jqXHR, textStatus, errorThrown) {
         alert(textStatus + ': ' + errorThrown);
      }).always(function(data) {
      });
}


$(document).on('click', '.add-sensor', function(e){
   var scheme = window.location.protocol
   var path = scheme + '//' + window.location.host + '/';
   url = path + `${id_facilidad}/sensor/`

   var parameters = new FormData(document.getElementById("sensorForm"))

   var skeleton_form = $('.clone').clone(true);
   $('.card-body-form').html("")
   $('.card-body-form').append(skeleton_form)
   skeleton_form.removeClass('d-none')

   $.ajax({
      url: url,
      method: 'POST',
      dataType: 'json',
      headers: {
         "X-CSRFToken": csrftoken,
      },
      data: parameters,
      processData: false,
      contentType: false,
      success: function(response){
         if (response.status == 200){
            $('.card-body-form').html("")
            $('.card-body-form').append(response.html_card)

         } else if (response.status == 400) {
            errors = JSON.parse(response.errors)

            if ($('input').next('p').length) $("input").nextAll('p').empty();
               for (var name in errors){
                  for (var i in errors[name]){
                     var $input = $('input[name='+name+']');
                     $input.after("<p style='color: #ff5f5fde;'>"+ errors[name][i].message+ "</p>");
                  }
               }
         }

         
      }
   })
})