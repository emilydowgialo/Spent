"use strict";

function showExpenditureResults(result) {

    // Callbacks
    updateTotalSpent(result);
    updateAverageSpent(result);
    appendExpenditure(result);
    updateProgressBars(result);
    charts();
}

function submitExpenditure(evt) {
    evt.preventDefault();

    // Close the modal via Javascript when the event is triggered
    $('#addExpenditureModal').modal('toggle');

    // Gather data from the form
    var formInputs = {
        "category": $("#category-field").val(),
        "price": $("#price").val(),
        "date": $("#date").val(),
        "wherebought": $("#wherebought").val(),
        "description": $("#description").val(),
        "tracking-num": $("#tracking-num").val(),
        "tracking-num-carrier": $("#tracking-num-carrier").val()
    };

    // Post info to this route to add to the database
    $.post("/add-expenditure-to-db",
           formInputs,
           showExpenditureResults
           );
}

function appendExpenditure(result) {
  // This function appends a new expenditure in the Expenditures widget

  var expenditure = result;

  // Begin HTML to append
  var stringToAppend = '<tr>' +
  '<th scope="row">' +
  String(expenditure.category) +
  '</th>' +
  '<td>' +
  String(expenditure.price) +
  '</td>' +
  '<td>' +
  String(expenditure.date_of_expenditure) +
  '</td>' +
  '<td>' +
  String(expenditure.where_bought) +
  '</td>' +
  '<td>' +
  String(expenditure.description) +
  '</td>' +
  '<td>';

  // If a tracking number exists, append this
  if (expenditure.tracking_num) {

    stringToAppend += '<form action="tracking/' + String(expenditure.tracking_num) +
    'method="POST" class="tracking-form"><button type="submit" class="btn btn-lg ' +
    'btn-custom" aria-label="Left Align" data-toggle="modal" data-target="#trackingModal" ' +
    'data-trackingnum="' + String(expenditure.tracking_num) + '">' +
    '<span class="glyphicon glyphicon-send" aria-hidden="true"></span>' +
    '</button></form>'
  }

  // Continue the HTML to append
  stringToAppend += '</td>' +
  '<td><form action="/remove-expenditure/' +
  String(expenditure.id) + '" method="POST" id="expenditure-' +
  String(expenditure.id) + '">' +
  '<button type="submit" class="btn btn-lg btn-custom" aria-label="Left Align">' +
  '<span class="glyphicon glyphicon-minus-sign" aria-hidden="true"></span>' +
  '</button>' +
  '</form></td>' +
  '</tr>';

  // Append the HTML at this ID
  console.log(stringToAppend);
  $('#table-expenditure-table').append(stringToAppend);
  console.log("finished with appendExpenditure");

}

function updateTotalSpent(result) {
  // This function updates the total amount spent on the front end

  // Contains information about the expenditure
  var expenditure = result;
  console.log(expenditure.total_cat_price);
  var stringToAppend = String(expenditure.total_cat_price);

  // This is the place to append the info
  var expenditureElement = $('#total-spent-' + String(expenditure.category_id));

  expenditureElement.html(stringToAppend);
  console.log("finished updateTotalSpent");

}

function updateAverageSpent(result) {
  // This function updates the average amount spent on the front end

  // Contains info about the average
  var average = result;
  console.log(average.avg_cat_expenditures);
  var stringToAppend = String(average.avg_cat_expenditures);

  // This is the place to append the info
  var avgElement = $('#avg-' + String(average.category_id));

  avgElement.html(stringToAppend);
  console.log("finished updateAverageSpent");

}

// Event listener
$("#expenditure-form").on("submit", submitExpenditure);