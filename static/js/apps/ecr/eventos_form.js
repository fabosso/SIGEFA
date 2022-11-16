var select_subtipo = $('select[name="subtipo"]');

window.lastStatus = {};
lastStatus.value = "";

const diccionario = {
  clasificaciones: {
    0: "publico",
    1: "publico",
    2: "reservado",
    3: "confidencial",
    4: "secreto",
  },
  precedencias: {
    0: "rutina",
    1: "rutina",
    2: "prioridad",
    3: "inmediato",
    4: "flash",
  },
  redes: {
    0: "Red Cdo Op",
    1:  "Red Cdo Op",
    2:  "Red Mat Pers",
    3:  "Red Cdo",
    4:  "Red Op",
  },

}

function descriptionMiddleware(formData) {
  if (formData.tipo !== "1") {
    return formData.description;
  }
  let newDescription = "";
  if (formData.subtipo !== "2") {
    newDescription = "ORIGEN: ";
  } else {
    newDescription = "DESTINO: ";
  }
  newDescription += diccionario.redes[formData.origen_destino] + "\n";
  newDescription += `CLASIFICACION: ${diccionario.clasificaciones[formData.clasificacion]}\n`;
  newDescription += `PRECEDENCIA: ${diccionario.precedencias[formData.precedencia]}\n`;
  newDescription += `EVENTO: transmitido\n`;
  newDescription += `MENSAJE: ${formData.description}\n`;
  newDescription += formData.cifrado === "1" ? "CIFRADO\n" : "";
  return newDescription;
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function change_color(status_to_change) {
  if (status_to_change == "S") {
    $("button[name='L']").removeClass("btn-warning").addClass("btn-secondary");
    $("button[name='F']").removeClass("btn-danger").addClass("btn-secondary");
    $("button[name=" + status_to_change + "]").addClass("btn-success");
  } else if (status_to_change == "L") {
    $("button[name='S']").removeClass("btn-success").addClass("btn-secondary");
    $("button[name='F']").removeClass("btn-danger").addClass("btn-secondary");
    $("button[name=" + status_to_change + "]").addClass("btn-warning");
  } else {
    $("button[name='S']").removeClass("btn-success").addClass("btn-secondary");
    $("button[name='L']").removeClass("btn-warning").addClass("btn-secondary");
    $("button[name=" + status_to_change + "]").addClass("btn-danger");
  }
}
const csrftoken = getCookie("csrftoken");

$(".select2").select2({
  theme: "bootstrap4",
  language: "es",
});

$(function () {
  $(".select2").select2({
    theme: "bootstrap4",
    language: "es",
  });

  $('select[name="tipo"]').on("change", function () {
    var id = $(this).val();

    var option = '<option  value="">---------</option>';
    if (id === "") {
      select_subtipo.html(option);
      return false;
    }

    $.ajax({
      url: url_search_type,
      type: "GET",
      data: {
        id: id,
      },
      dataType: "json",
    })
      .done(function (data) {
        if (!data.hasOwnProperty("error")) {
          select_subtipo.html("").select2({
            theme: "bootstrap4",
            language: "es",
            data: data,
          });
          return false;
        }
      })
      .fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ": " + errorThrown);
      })
      .always(function (data) {});
  });
});

$(".post-evento-button").on("click", function (e) {
  e.preventDefault();
  var event_form_data = new FormData(document.getElementById("EventosForm"));

  var ws_scheme = window.location.protocol;
  var path = ws_scheme + "//" + window.location.host + "/";
  var id_facilidad = $("#id_facilidad").text();

  url = path + `${id_facilidad}/eventos`;

  let formData = {};
  for (const pair of event_form_data.entries()) {
    formData[pair[0]] = pair[1];
  }

  event_form_data.set("description", descriptionMiddleware(formData));
  for (const pair of event_form_data.entries()) {
    console.log(`${pair[0]}, ${pair[1]}`);
  }

  $.ajax({
    url: url,
    type: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    data: event_form_data,
    dataType: "json",
    cache: false,
    processData: false,
    contentType: false,
  })
    .done(function (response) {
      if (response.status == 200) {
        $("#EventosForm").trigger("reset");
        Swal.fire({
          position: "center",
          icon: "success",
          title: response["message"],
          showConfirmButton: false,
          timer: 5500,
        });
        if (section == "Libro de Guardia") {
          get_datatable(get_list_url(current_page));
        }
        setTimeout(() => {
          window.location.reload();
        }, 2000);
      }
    })
    .fail(function (jqXHR, textStatus, errorThrown) {
      alert(textStatus + ": " + errorThrown);
    })
    .always(function (response) {});
});

$(".status-btn").on("click", function (e) {
  var status_to_change = $(this).attr("name");
  var id_facilidad = $("#id_facilidad").text();

  $.confirm({
    theme: "bootstrap",
    title: "¡¡¡Atencion!!!",
    icon: "fas fa-exclamation-circle",
    alignMiddle: true,
    type: "red",
    content: "¿Está seguro que desea modificar el estado de alistamiento?",
    typeAnimated: true,
    buttons: {
      Confirmar: {
        btnClass: "btn-danger",
        action: function () {
          var ws_scheme = window.location.protocol;
          var path = ws_scheme + "//" + window.location.host + "/";
          url = path + `change/facilidad_status/`;

          $.ajax({
            type: "POST",
            url: url,
            headers: {
              "X-CSRFToken": csrftoken,
            },
            data: {
              id: id_facilidad,
              status: status_to_change,
            },
            dataType: "json",
            success: function (response) {
              Swal.fire({
                position: "center",
                icon: "success",
                title: response["message"],
                showConfirmButton: false,
                timer: 5500,
              });
              change_color(status_to_change);
            },
            error: function (response) {
              Swal.fire({
                title: "Error!",
                html: response["error"],
                icon: "error",
              });
            },
          });
        },
      },
      Cancelar: function () {},
    },
  });
});

$(document).ready(function () {
  window.setInterval(function () {
    var path = window.location.protocol + "//" + window.location.host + "/";
    var id_facilidad = $("#id_facilidad").text();
    var url_status = path + "api/facilidad/" + id_facilidad + "/status";
    $.ajax({
      type: "GET",
      url: url_status,
      success: function (response) {
        if (lastStatus.value !== response.status) {
          lastStatus.value = response.status;
          change_color(response.status);
        }
      },
    });
  }, 1000);
});
