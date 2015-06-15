
var date_obj = new Date;
var amount = '1920';
var category = 8;
var description = '';

function formatDateString(d) {
  return d.getFullYear(4) + '-' + (('0'+(1+d.getMonth())).substr(-2)) 
         + '-' + ('0' + d.getDate(2)).substr(-2);
}

function incrementDate(d) {
  return d.setDate(d.getDate() + 1);
}

function decrementDate(d) {
  return d.setDate(d.getDate() - 1);
}

var date = formatDateString(date_obj);

function validateInput(value) {
  var re = /^[0-9]+[a-zA-Z]+$|^[a-zA-Z]+[0-9]+$/
  // var re = /^[0-9]+[a-zA-Z]+$/
  // var re = /^\D*?(\d+)\D*?$/
  if (re.test(value)) {
    return true;
  }
}

$(document).ready(function() {

  $( '#date-preview ').text(date);

  $( '.table-container' ).on('click', '.delete-link', function(event) {

    console.log("Click registered");

    var rowId = $(this).attr('name');
    var jsonData = [
      {"name":"command","value":"delete"},
      {"name":"id","value":rowId}
    ];

    console.log(JSON.stringify(jsonData));

    var pathname = window.location.pathname;

    $.post( pathname, jsonData, function(response) {
      $('.table-container').html(response);
    });
  }); 



});



/*$( '#input-box ').keyup(function(e) {

  // if user presses a-z or A-Z
  var code = e.keyCode || e.which;
  if (code >= 65 && code <= 90) {
    // e
    if (code == 69) {
      // $( '#input-form' ).submit({'cat':8}, e);
      // $( '#input-form' ).submit();
    }
  }

});*/