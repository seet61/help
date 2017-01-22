$('.datepicker').pickadate({
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 15, // Creates a dropdown of 15 years to control year
    firstDay: true//,
    // Months and weekdays
    //monthsFull: [ 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июня', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь' ],
    //monthsShort: [ 'Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек' ],
    //weekdaysFull: [ 'Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота' ],
    //weekdaysShort: [ 'Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб' ],
    // Materialize modified
    //weekdaysLetter: [ 'В', 'П', 'В', 'С', 'Ч', 'П', 'С' ],
    // Today and clear
    //today: 'Сегод.',
    //clear: 'Сброс',
    //close: 'Закр.'
});
$(document).ready(function(){
    $('ul.tabs').tabs();
});