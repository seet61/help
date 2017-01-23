$('.datepicker').pickadate({
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 10, // Creates a dropdown of 15 years to control year
    firstDay: true,
    closeOnSelect: true,
    closeOnClear: false
});
$(document).ready(function(){
    $('ul.tabs').tabs();
});