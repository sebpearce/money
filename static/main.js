
var date_obj = new Date;
var amount = '1920';
var category = 8;
var description = '';
var source = 1;

// check if integer (excludes strings)
function isIntNotString(x) {
  return (typeof x === 'number' && (x % 1) === 0);
}

function formatDateString(d) {
  return d.getFullYear(4) + '-' + (('0'+(1+d.getMonth())).substr(-2)) 
         + '-' + ('0' + d.getDate(2)).substr(-2);
}

function formatAsMoney(x) {
  return parseFloat(x/100).toFixed(2).replace(/(\d)(?=(\d{3})+\.)/g, '$1,');
}

function incrementDate(d, times) {
  times = times ? times : 1;
  return d.setDate(d.getDate() + times);
}

function decrementDate(d, times) {
  times = times ? times : 1;
  return d.setDate(d.getDate() - times);
}

var date = formatDateString(date_obj);

function validateInput(value) {
  var re = /^([0-9]+)([a-zA-Z]*)$/ // same as processInput
  // var re = /^[0-9]+[a-zA-Z]+$|^[a-zA-Z]+[0-9]+$/
  // var re = /^[0-9]+[a-zA-Z]+$/
  // var re = /^\D*?(\d+)\D*?$/
  if (re.test(value) && value != '') {
    return true;
  }
}

function validateVariables() {
  // validate date
  var date_re = /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/
  // validate amount
  var amt_re = /^[0-9]+$/

  return (date_re.test(date) && amt_re.test(amount) && isIntNotString(category));  
}

function updateOneRow(rowId, field, value) {

    var jsonData = [
      {"name":"command", "value":"update"},
      {"name":"id", "value": rowId},
      {"name":"field", "value": field},
      {"name":"value", "value": value}
    ];

    console.log(JSON.stringify(jsonData));

    var pathname = window.location.pathname;

    $.post( pathname, jsonData, function(response) {
      $('.table-container').html(response);
    });
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


