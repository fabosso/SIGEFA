let timer,
  timeoutVal = 1000;

$(document).on("input", ".slider-range", function () {
  window.clearTimeout(timer);

  id = $(this).attr("id");
  $("." + id + "").text($(this).val());

  timer = window.setTimeout(() => {
    parameters = $(this).serializeArray();

    $.ajax({
      url: window.location.href,
      type: "POST",
      dataType: "json",
      data: parameters,
      success: function (response) {
        if (response.status == 200) {
          //console.log(response);
          //console.log("200");
        } else {
          //console.log(response);
          //console.log("Error");
        }
      },
      error: function (response) {
        //console.log(response);
      },
    });
  }, timeoutVal);
});
