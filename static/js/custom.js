$('.datepicker').pickadate({
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 10, // Creates a dropdown of 15 years to control year
    firstDay: true
});
$('#timepicker').pickatime({
    default: 'now',
    autoclose: true,
    twelvehour: false,
    donetext: 'OK'
});
$('.collapsible').collapsible({
    accordion : false // A setting that changes the collapsible behavior to expandable instead of the default accordion style
});
// the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
$('.modal-trigger').leanModal();
$('.modal').modal({
    dismissible: true // Modal can be dismissed by clicking outside of the modal
});
$(document).ready(function(){
    $('ul.tabs').tabs();
});
