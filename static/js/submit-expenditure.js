"use strict";

function showExpenditureResults(result) {
    alert(result);
    updateTotalSpent(result);
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

$("#expenditure-form").on("submit", submitExpenditure);