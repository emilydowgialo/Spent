"use strict";

function showExpenditureResults(result) {
    updateTotalSpent(result);
    updateAverageSpent(result);
    appendExpenditure(result);
}

function submitExpenditure(evt) {
    evt.preventDefault();

    var formInputs = {
        "category": $("#category-field").val(),
        "price": $("#price").val(),
        "date": $("#date").val(),
        "wherebought": $("#wherebought").val(),
        "description": $("#description").val(),
        "tracking-num": $("#tracking-num").val(),
        "tracking-num-carrier": $("#tracking-num-carrier").val()
    };

    $.post("/add-expenditure-to-db",
           formInputs,
           showExpenditureResults
           );
}

function appendExpenditure(result) {

  var expenditure = result;

  var stringToAppend = '<form action="/remove-expenditure/' + String(expenditure.expenditure_id) +
  '" method="POST" id="expenditure-' + String(expenditure.expenditure_id) + '">' +
  String(expenditure.date_of_expenditure) +
  '<br>' +
  String(expenditure.category) +
  '<br>' +
  String(expenditure.price) +
  '<br>' +
  String(expenditure.where_bought) +
  '<br>' +
  String(expenditure.description) +
  '<br>' +
  String(expenditure.tracking_num)+
  '<br>' +
  '<input type="Submit" value="Remove">' +
  '</form>' +
  '<br>' +
  '<form action="/tracking/' + String(expenditure.tracking_num) + '" method="POST" id="tracking-form">' +
  '<input type="submit" value="Track Your Package">' +
  '<br>' +
  '</form>';

  console.log(stringToAppend);
  $('#expenditures-div').append(stringToAppend);
  console.log("finished with appendExpenditure");

}

function updateTotalSpent(result) {

  var expenditure = result;
  console.log(expenditure.total_cat_price);
  var stringToAppend = String(expenditure.total_cat_price);

  var expenditureElement = $('#total-spent-' + String(expenditure.category_id));

  expenditureElement.html(stringToAppend);
  console.log("finished updateTotalSpent");

}

function updateAverageSpent(result) {

  var average = result;
  console.log(average.avg_cat_expenditures);
  var stringToAppend = String(average.avg_cat_expenditures);

  var avgElement = $('#avg-' + String(average.category_id));

  avgElement.html(stringToAppend);
  console.log("finished updateAverageSpent");

}

$("#expenditure-form").on("submit", submitExpenditure);