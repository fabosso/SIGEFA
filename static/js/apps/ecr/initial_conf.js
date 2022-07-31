var hideable_selecte_form1 = $(".hideable-select-form1");
var hideable_selecte_form2 = $(".hideable-select-form2");

hideable_selecte_form1.hide();
hideable_selecte_form2.hide();

$("#hidden-spinner").hide();

$("#InputLabel").html("Equipo Com 1:");

$("input[name=comunicaciones_options]").on("click", function (e) {
  var value = $(this).val();

  if (value == "1") {
    hideable_selecte_form2.hide();
    hideable_selecte_form1.show("slow");
  } else {
    hideable_selecte_form1.hide();
    hideable_selecte_form2.show("slow");
  }
});

function updateElementIndex(el, prefix, ndx) {
  var id_regex = new RegExp("(" + prefix + "-\\d+)");
  var replacement = prefix + "-" + ndx;

  if ($(el).attr("for"))
    $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
  if (el.id) el.id = el.id.replace(id_regex, replacement);
  if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function cloneMore(selector, prefix) {
  var newElement = $(selector).clone(true);
  var total = $("#id_" + prefix + "-TOTAL_FORMS").val();

  newElement
    .find(":input:not([type=button]):not([type=submit]):not([type=reset])")
    .each(function () {
      var name = $(this)
        .attr("name")
        .replace("-" + (total - 1) + "-", "-" + total + "-");
      var id = "id_" + name;
      $(this).attr({ name: name, id: id }).val("").removeAttr("checked");
    });

  newElement
    .find(".col-4")
    .children()
    .each(function () {
      var forValue = $(this)[0]["innerHTML"];
      if (forValue) {
        v = parseInt(total) + 1;
        newValue = "Equipo Com " + v + ":";
        $(this).html(newValue);
      }
    });

  total++;

  $("#id_" + prefix + "-TOTAL_FORMS").val(total);
  $(selector).after(newElement);
  var conditionRow = $(".form-row:not(:last)");

  conditionRow
    .find(".btn.add-form-row")
    .removeClass("btn-success")
    .addClass("btn-danger")
    .removeClass("add-form-row")
    .addClass("remove-form-row")
    .html('<span class="fas fa-trash" aria-hidden="true"></span>');

  return false;
}

function deleteForm(prefix, btn) {
  var total = parseInt($("#id_" + prefix + "-TOTAL_FORMS").val());

  if (total > 1) {
    btn.closest(".form-row").remove();
    var forms = $(".form-row");

    $("#id_" + prefix + "-TOTAL_FORMS").val(forms.length);
    for (var i = 0, formCount = forms.length; i < formCount; i++) {
      $(forms.get(i))
        .find(":input")
        .each(function () {
          $(forms.get(i))
            .find(".col-4")
            .children()
            .each(function () {
              var forValue = $(this)[0]["innerHTML"];
              if (forValue) {
                v = i + 1;
                newValue = "Equipo Com " + v + ":";
                $(this).html(newValue);
              }
            });
          updateElementIndex(this, prefix, i);
        });
    }
  }
  return false;
}

$(document).on("click", ".add-form-row", function (e) {
  e.preventDefault();
  cloneMore(".form-row:last", "form");
  return false;
});

$(document).on("click", ".remove-form-row", function (e) {
  e.preventDefault();
  deleteForm("form", $(this));
  return false;
});

$(document).ready(function () {
  $(".confInitButton").click(function (e) {
    e.preventDefault();
    var parameters = new FormData(document.getElementById("ConfInitForm"));

    $(".confInitButton").hide();
    $("#hidden-spinner").show();

    $.ajax({
      url: window.location.href,
      type: "POST",
      dataType: "json",
      data: parameters,
      processData: false,
      contentType: false,
      success: function (response) {
        if (response.status == 200) {
          url = response.success_url;
          window.location.assign(url);
        } else if (response.status == 400) {
          errors_array = response.errors;
          $("#hidden-spinner").hide();
          $(".confInitButton").show();

          if ($("input").next("p").length) $("input").nextAll("p").empty();
          if ($("select").next("p").length) $("select").nextAll("p").empty();

          for (
            var i = 0, errorCount = errors_array.length;
            i < errorCount;
            i++
          ) {
            err_obj = JSON.parse(errors_array[i]);
            console.log(err_obj);
            for (var name in err_obj) {
              for (var j in err_obj[name]) {
                var $input = $("input[name=" + name + "]");
                var $select = $("select[name=" + name + "]");
                $input.after(
                  "<p style='color: #ff5f5fde;'>" +
                    err_obj[name][j].message +
                    "</p>"
                );
                $select.after(
                  "<p style='color: #ff5f5fde;'>" +
                    err_obj[name][j].message +
                    "</p>"
                );
              }
            }
          }
        } else if (response.status == 500) {
          console.log(response);
        }
      },
      error: function (response) {
        console.log(response);
      },
    });
  });
});
