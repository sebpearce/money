// bind date shortcuts [ and ]

$(document).bind('keydown', '[', function(e){
    decrementDate(date_obj, 1);
    date = formatDateString(date_obj);
    $(' #date-preview ').text(date);
});
$(' #input-box ').bind('keydown', '[', function(e){
    decrementDate(date_obj, 1);
    date = formatDateString(date_obj);
    $(' #date-preview ').text(date);
    e.stopPropagation();
    e.preventDefault();
});
$(document).bind('keydown', 'shift+[', function(e){
    decrementDate(date_obj, 10);
    date = formatDateString(date_obj);
    $(' #date-preview ').text(date);
});
$(' #input-box ').bind('keydown', 'shift+[', function(e){
    decrementDate(date_obj, 10);
    date = formatDateString(date_obj);
    $(' #date-preview ').text(date);
    e.stopPropagation();
    e.preventDefault();
});
$(document).bind('keydown', ']', function(e){
    incrementDate(date_obj, 1);
    date = formatDateString(date_obj);
    $(' #date-preview ').text(date);
});
$(' #input-box ').bind('keydown', ']', function(e){
    incrementDate(date_obj, 1);
    date = formatDateString(date_obj);
    $(' #date-preview ').text(date);
    e.stopPropagation();
    e.preventDefault();
});
$(document).bind('keydown', 'shift+]', function(e){
    incrementDate(date_obj, 10);
    date = formatDateString(date_obj);
    $(' #date-preview ').text(date);
});
$(' #input-box ').bind('keydown', 'shift+]', function(e){
    incrementDate(date_obj, 10);
    date = formatDateString(date_obj);
    $(' #date-preview ').text(date);
    e.stopPropagation();
    e.preventDefault();
});

// bind enter key to submit button even when outside input box
$(document).bind('keydown', 'enter', function(e){
  $( '#input-form' ).submit();
});


$( '#input-box' ).on('input', function(){

  var val = $(this).val();
  console.log(val);
  processInput(val);

});

$( 'input' ).click(function(){
  this.select();
});

$(' .category-select ').on('change', function(){

  alert(this.value);

});

$(' #category-select-preview ').on('change', function(){

  category = parseInt(this.value, 10);
  console.log("category set to ", category);
  $( '#category-preview ').text(categoryNames[category]);
  this.blur();
  $( '#input-box' ).focus();

});

$(' #source-select-preview ').on('change', function(){

  source = parseInt(this.value, 10);
  console.log("source set to ", source);
  $( '#source-preview ').text(sourceNames[source]);
  this.blur();
  $( '#input-box' ).focus();

});


$( '#input-form' ).submit(function(event) {

  if (validateInput && validateVariables()) {

    var jsonData = [
    {"name":"command","value":"insert"},
    {"name":"date","value":date},
    {"name":"amount","value":amount},
    {"name":"category","value":category},
    {"name":"source","value":source},
    {"name":"description","value":description}
    ];

    console.log(JSON.stringify(jsonData));

    var pathname = window.location.pathname;

    $.post( pathname, jsonData, function(response) {
      $('.table-container').html(response);
    });

    $( '#input-box' ).val('');
    $( '#amount-preview ').text('');
    event.preventDefault();

    $( '#input-box' ).focus();
    amount = 0;

  }  else {
    console.log('Validation failed');
    return false;
  }

});
