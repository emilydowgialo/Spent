
function shutdownIntercom () {

	Intercom('shutdown');
	
}

// Button click event
$('#sign-out').click(shutdownIntercom);