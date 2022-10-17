var id_facilidad = $("#id_facilidad").text();
var id_sensor = $("#id_sensor").text();

function obtain_title(line) {
  const index = line.indexOf("(");
  return line.substring(0, index);
}

function obtain_unit(line) {
  const index = line.indexOf("(");
  return line.substring(index + 1, index + 2);
}

function obtain_value(line) {
  const index = line.indexOf(")");
  return line.substring(index + 1).trim();
}

function create_sensor_card(nombre, valor) {
  
  card = `<div class="row justify-content-center text-center">`;
  card += `<div class="col-md-6 mb-3">`;
  card += `<h4>${nombre}</h4>`;
  card += `<p>${valor}</p>`;
  card += `</div></div>`;

  return card;
}

if (sensor_created == "True") {
  const scheme = window.location.protocol;
  const path = scheme + "//" + window.location.host + "/";
  const sensores = [1, 2, 3, 6];
  sensores.forEach((sensor) => {
    const classToChange = `.card-sensor-${sensor}`;
    url = path + `api/facilidad/${id_facilidad}/sensor/${sensor}/edit/`;

    var skeleton_form = $(".clone").clone(true);
    $(classToChange).html("");
    $(classToChange).append(skeleton_form);
    skeleton_form.removeClass("d-none");

    $.ajax({
      url: url,
      method: "GET",
    })
      .done((data) => {
        const title = obtain_title(data.nombre);
        const unit = obtain_unit(data.nombre);
        const value = data.indicador;
        const valor = unit === "°" ? `${value} ${unit}C` : `${value} ${unit}`;
        $(classToChange).html("");
        const card = create_sensor_card(title, valor);
        $(classToChange).append(card);
      })
      .fail((jqXHR, textStatus, errorThrown) => {
        alert(textStatus + ": " + errorThrown);
      });
  });
}

$(document).on("click", ".add-sensor", function (e) {
  var scheme = window.location.protocol;
  var path = scheme + "//" + window.location.host + "/";
  url = path + `${id_facilidad}/sensor/`;

  var parameters = new FormData(document.getElementById("sensorForm"));

  var skeleton_form = $(".clone").clone(true);
  $(".card-body-form").html("");
  $(".card-body-form").append(skeleton_form);
  skeleton_form.removeClass("d-none");

  $.ajax({
    url: url,
    method: "POST",
    dataType: "json",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    data: parameters,
    processData: false,
    contentType: false,
    success: function (response) {
      if (response.status == 200) {
        $(".card-body-form").html("");
        $(".card-body-form").append(response.html_card);
      } else if (response.status == 400) {
        errors = JSON.parse(response.errors);

        if ($("input").next("p").length) $("input").nextAll("p").empty();
        for (var name in errors) {
          for (var i in errors[name]) {
            var $input = $("input[name=" + name + "]");
            $input.after(
              "<p style='color: #ff5f5fde;'>" + errors[name][i].message + "</p>"
            );
          }
        }
      }
    },
  });
});

$(document).ready(function(){
  window.setInterval(function() {
    var path = window.location.protocol + "//" + window.location.host + "/";
    var id_facilidad = $("#id_facilidad").text();
    const sensores = [1, 2, 3, 6];
    sensores.forEach((sensor) => {
      url = path + `api/facilidad/${id_facilidad}/sensor/${sensor}/edit/`;
      $.ajax({
        url: url,
        method: "GET",
        success: function (response) {
          const classToChange = `.card-sensor-${sensor}`;
          const line = $(classToChange).text();
          const lines = line.split(" ");
          const title = lines[0] + " ";
          let valor;
          if (lines[2]) {
            valor = response.indicador + " " + lines[2];
          } else {
            valor = response.indicador;
          }
          $(classToChange).html("");
          const card = create_sensor_card(title, valor);
          $(classToChange).append(card);
        }
      })
    });
  }, 2000);
});