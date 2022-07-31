var id_facilidad = $("#id_facilidad").text();
var id_sensor = $("#id_sensor").text();

function create_sensor_card(data) {
  card = `<div class="row justify-content-center text-center">`;
  card += `<div class="col-md-6 mb-3">`;
  card += `<h4>${data.nombre}</h4>`;
  card += `<p>${data.indicador}</p>`;
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
        console.log(data);
        $(classToChange).html("");
        card = create_sensor_card(data);
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
