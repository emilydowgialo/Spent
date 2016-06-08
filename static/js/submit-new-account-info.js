/* global $*/
"use strict";

function replaceInfo(results) {

    // Close the modal via Javascript when the event is triggered
    $('#add-account-modal').modal('toggle');

    // The results contain the new name and email, if provided
    var newInfo = results;

    console.log(newInfo);

    var newName = String(newInfo.name);
    var newEmail = String(newInfo.email);

    // This is the element to edit
    var nameElement = $('#user-name');
    var emailElement = $('#user-name');

    // Changes the info
    nameElement.html(newName);
    emailElement.html(newEmail);
    console.log("finished replaceInfo");
}

function updateAccountInfo(evt) {
    evt.preventDefault();

    // Close the modal via Javascript when the event is triggered
    $('#editProfile').modal('toggle');

    // Gather info from the form
    var info = $('#form-profile-edit').serialize();

    // Parse form information, which returns information jsonified
    $.post('/profile-edit', info, replaceInfo);
    console.log("Finished sending AJAX");
}

// Submit button click event
$('#submit-new-account-info').click(updateAccountInfo);