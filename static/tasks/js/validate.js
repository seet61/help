function validate_post() {
	//color for labels red darken-2

	if ($("#number").val() === "") {
		//console.log('number "' + $("#number").val() + '"');
		var number = false;
	} else {
		var number = true;
	}

	if ($("#calendar").val() == "") {
		//console.log('calendar "' + $("#calendar").val() + '"');
		var calendar = false;
	} else {
		var calendar = true;
	}

	if ($("#comment").val() == "") {
		//console.log('comment "' + $("#comment").val() + '"');
		var comment = false;
	} else {
		var comment = true;
	}

	if (number & calendar & comment) {
		alert('number: ' + number + 'calendar: ' + calendar + 'comment: ' + comment + ' Все поля заполены');
		//$.post({% url 'post_task' %});
	} else {
		Materialize.toast('Заполнены не все поля!', 4000);
		alert();
	}
}