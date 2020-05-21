window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

$(document).ready(function () {
  $("#start_time").blur(function (e) {
    const id = document.getElementById('artist_id').value;
    value = $("#start_time").val().split(' ');
    console.log(value);
    
    fetch('/artists/' + id + '/aviliability/check', {
      method: 'POST',
      body: JSON.stringify({
        'start_time': value[0],
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => response.json())
      .then(jsonResponse => {
        console.log(jsonResponse.valid)
        if (!jsonResponse.valid) {
          console.log("in if");
          document.getElementById("error").className = '';
        } else {
          console.log("else");
          document.getElementById("error").className = "hidden";
        }
      })
  })
})


$(document).ready(function () {
  $('#checkbox :checkbox').attr('checked', false);

  $('#checkbox :checkbox').change(function () {
    if (this.checked) {
      $('#desc').removeClass("hidden");
    } else {
      $('#desc').addClass("hidden");
    }
  })
  $('#end_date, #start_date').attr({
    min: $('#start_date').val(),
    max: '2050-12-31'
  });
  $('#end_date').blur(function () {
    var begD = $('#start_date').val();
    var endD = $('#end_date').val();

    if (new Date(begD) > new Date(endD)) {
      $('#end_date').val('')
    }
  });

});
