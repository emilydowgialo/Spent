
function shutdownIntercom () {

	evt.preventDefault();

	Intercom('shutdown');
	$.post('/add-budget');

}

// Button click event
$('#sign-out').click(shutdownIntercom);