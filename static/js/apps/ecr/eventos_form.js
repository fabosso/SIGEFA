var select_subtipo = $('select[name="subtipo"]');



function getCookie(name) {
   let cookieValue = null;
   if (document.cookie && document.cookie !== '') {
       const cookies = document.cookie.split(';');
       for (let i = 0; i < cookies.length; i++) {
           const cookie = cookies[i].trim();
           // Does this cookie string begin with the name we want?
           if (cookie.substring(0, name.length + 1) === (name + '=')) {
               cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
               break;
           }
       }
   }
   return cookieValue;
}
const csrftoken = getCookie('csrftoken');


$('.select2').select2({
   theme: 'bootstrap4',
   language: 'es',
})

$(function () {
      $('.select2').select2({
         theme: 'bootstrap4',
         language: 'es',
      });

      $('select[name="tipo"]').on('change', function (){
         var id = $(this).val();

         var option = '<option  value="">---------</option>';
         if (id === ''){
            select_subtipo.html(option);
            return false;
         }

         $.ajax({
            url: url_search_type,
            type: 'GET',
            data: {
               'id': id,
            },
            dataType: 'json',
         }).done(function(data){
            if (!data.hasOwnProperty('error')) {
               select_subtipo.html('').select2({
                     theme: 'bootstrap4',
                     language: 'es',
                     data: data
                  });
                  return false;
               }

         }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
         }).always(function(data) {

         });

   });
});

$('.post-evento-button').on('click', function(e){
      e.preventDefault()
      var event_form_data = new FormData(document.getElementById("EventosForm"));

      var ws_scheme = window.location.protocol
      var path = ws_scheme + '//' + window.location.host + "/";
      var id_facilidad = $('#id_facilidad').text()

      url = path + `${id_facilidad}/eventos`;

      $.ajax({
         url: url,
         type: 'POST',
         headers: {
            "X-CSRFToken": csrftoken,
         },
         data: event_form_data,
         dataType: 'json',
         cache: false,
         processData: false,
         contentType: false,
      }).done(function(response){
         
         if (response.status == 200){
               $('#EventosForm').trigger("reset");
               Swal.fire({
                  position: 'center',
                  icon: 'success',
                  title: response['message'],
                  showConfirmButton: false,
                  timer: 5500
              })
              if (section == "Libro de Guardia"){
                  get_datatable(get_list_url(current_page));
              }  
         }
      }).fail(function (jqXHR, textStatus, errorThrown) {
         alert(textStatus + ': ' + errorThrown);
      }).always(function(response) {

   });

});


$(".status-btn").on('click', function(e){
   var status_to_change = $(this).attr('name')
   var id_facilidad = $('#id_facilidad').text()

   $.confirm({
      theme: 'bootstrap',
      title: '¡¡¡Atencion!!!',
      icon: 'fas fa-exclamation-circle',
      alignMiddle: true,
      type: 'red',
      content: 'Estas seguro que desea modificar el estado de alistamiento?',
      typeAnimated: true,
      buttons: {
         Confirmar: {
            btnClass: 'btn-danger',
            action: function(){
               var ws_scheme = window.location.protocol
               var path = ws_scheme + '//' + window.location.host + "/";
               url = path + `change/facilidad_status/`;
               
               $.ajax({
                  type: "POST",
                  url: url,
                  headers: {
                     "X-CSRFToken": csrftoken,
                  },
                  data : {
                     'id': id_facilidad,
                     'status': status_to_change,
                  },
                  dataType: 'json',
               success: function (response) {
                  Swal.fire({
                     position: 'center',
                     icon: 'success',
                     title: response['message'],
                     showConfirmButton: false,
                     timer: 5500
                 })

                 if  (status_to_change == 'S'){
                  $("button[name='L']").removeClass("btn-warning").addClass("btn-secondary");
                  $("button[name='F']").removeClass("btn-danger").addClass("btn-secondary");
                    $("button[name="+status_to_change+"]").addClass("btn-success");
                 } else if (status_to_change == 'L') {
                  $("button[name='S']").removeClass("btn-success").addClass("btn-secondary");
                  $("button[name='F']").removeClass("btn-danger").addClass("btn-secondary");
                  $("button[name="+status_to_change+"]").addClass("btn-warning");
                 } else {
                  $("button[name='S']").removeClass("btn-success").addClass("btn-secondary");
                  $("button[name='L']").removeClass("btn-warning").addClass("btn-secondary");
                  $("button[name="+status_to_change+"]").addClass("btn-danger");
                 }
                 
               },
              error: function (response) {
                  Swal.fire({
                     title: 'Error!',
                     html: response['error'],
                     icon: 'error'
                  });
              }
            }); 


            }
        },
         

            



 
          
          Cancelar: function () {

          },
      }
  });

});