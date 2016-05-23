"use strict";

function showExpenditureResults(result) {
    updateTotalSpent(result);
    updateAverageSpent(result);
}

function submitExpenditure(evt) {
    evt.preventDefault();

    var formInputs = {
        "category": $("#category-field").val(),
        "price": $("#price").val(),
        "date": $("#date").val(),
        "wherebought": $("#wherebought").val(),
        "description": $("#description").val()
    };

    $.post("/add-expenditure-to-db",
           formInputs,
           showExpenditureResults
           );
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