$('.datepicker').pickadate({
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 10, // Creates a dropdown of 15 years to control year
    firstDay: true,
    onSet: function () {
   		this.close();
	}
});
$('#timepicker').pickatime({
    default: 'now',
    autoclose: true,
    twelvehour: false,
    donetext: 'OK'
});
$(document).ready(function(){
    $('ul.tabs').tabs();
});