function deleteExpenOnPage(result) {
    // This function will delete the expenditure row on the dashboard

    // Get the expenditure id
    var id = result;
    console.log("this is id");
    console.log(id);

    expenId = id.expenditure_id;

    console.log("this is expenId");
    console.log(expenId);

    // Remove that expenditure row
    $('#expenditure-row-' + String(expenId)).remove();

    console.log("delete expen on page function ran");
}

function deleteExpenditure(evt) {
    evt.preventDefault();

    // Get the expenditure ID
    var id = $(evt.target).data("expenditureid");

    console.log("this is evt target");
    console.log(evt.target);

    console.log("this is id");
    console.log(id);

    // Post the id information to the remove expenditure route and call
    // the function that will remove that row from the front end
    $.post("/remove-expenditure/" + String(id), deleteExpenOnPage);
    console.log("ran deleteExpenditure");
}

// When this button is pressed, call the deleteExpenditure function
$(".delete-expenditure").click(deleteExpenditure);