var current_page = 1;

$("#hidden-spinner").hide();

function get_list_url(page) {
  var ws_scheme = window.location.protocol;
  var path = ws_scheme + "//" + window.location.host + "/";
  var id_facilidad = $("#id_facilidad").text();

  url = path + `api/facilidad/${id_facilidad}/eventos/list?page=${page}`;
  return url;
}

function putTableData(data) {
  let row;
  $("#eventos_tbody").html("");
  tbody = $("#eventos_tbody");

  if (data["results"].length > 0) {
    $.each(data["results"], function (a, b) {
      row =
        "<tr id=" +
        b.id +
        " scope='row'><td>" +
        b.id +
        "</td>" +
        "<td>" +
        b.tipo +
        "</td>" +
        "<td>" +
        b.subtipo +
        "</td>" +
        "<td>" +
        b.description +
        "</td>" +
        "<td>" +
        b.timestamp +
        "</td>";
      tbody.append(row);
    });
  } else {
    $("#eventos_tbody").html("No results found.");
  }

  pagination = create_pagination_control(data);
  $(".pagination-box").html("");
  $(".pagination-box").append(pagination);
}

function create_pagination_control(data) {
  previous_url = data.links.previous;
  next_url = data.links.next;
  page_links = data.page_links.page_links;

  ul = '<ul class="pagination" style="margin: 5px 0 10px 0">';

  if (previous_url) {
    li = `<li>
               <button  class="page-link" data-url="${previous_url}" aria-label="Previous">
                  <span aria-hidden="true">&laquo;</span>
               </button>
            </li>`;
  } else {
    li = `<li class="page-item disabled">
               <button  class="page-link" aria-label="Previous">
                  <span aria-hidden="true">&laquo;</span>
               </button>
            </li>`;
  }
  ul += li;

  $.each(page_links, function (id, page) {
    if (page.is_break) {
      li2 = `<li class="page-item disabled">
                  <button class="page-link"><span aria-hidden="true">&hellip;</span></button>
               </li>`;
    } else {
      if (page.is_active) {
        li2 = `<li class="page-item active">
                     <button class="page-link" id="button-${id}" data-url="${page.url}">${page.number}</button>
                  </li>`;
      } else {
        li2 = `<li>
                     <button class="page-link" id="button-${id}" data-url="${page.url}">${page.number}</button>
                  </li>`;
      }
    }
    ul += li2;
  });

  if (next_url) {
    li3 = `<li>
               <button class="page-link" data-url="${next_url}" aria-label="Next">
                  <span aria-hidden="true">&raquo;</span>
               </button>
            </li>`;
  } else {
    li3 = `<li class="page-item disabled">
               <button class="page-link" aria-label="Next">
                  <span aria-hidden="true">&raquo;</span>
               </button>
            </li>`;
  }
  ul += li3;
  ul += `</ul>`;

  return ul;
}

$(document).on("click", ".page-link", function (e) {
  e.preventDefault();
  let url = $(this).attr("data-url");

  $("body,html").animate(
    {
      scrollTop: 0,
    },
    600
  );

  get_datatable(url);
});

function get_datatable(url) {
  $("#eventos_tbody").html("");
  $("#hidden-spinner").show();

  $.ajax({
    url: url,
    method: "GET",
  })
    .done(function (data) {
      console.log(data);
      $("#hidden-spinner").hide();
      current_page = parseInt(data.links.current);
      putTableData(data);

      $("#result-count span").html(data.count);

      if (data.links.current == null) {
        $("#page-count span").html("1");
      } else {
        $("#page-count span").html(data.links.current);
      }
    })
    .fail(function (jqXHR, textStatus, errorThrown) {
      alert(textStatus + ": " + errorThrown);
    })
    .always(function (data) {});
}

get_datatable(get_list_url(current_page));
