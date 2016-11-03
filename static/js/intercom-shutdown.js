
function shutdownIntercom (evt) {

	evt.preventDefault();

	Intercom('shutdown');
	window.location = '/logout';

}

// Button click event
$('#sign-out').click(shutdownIntercom);