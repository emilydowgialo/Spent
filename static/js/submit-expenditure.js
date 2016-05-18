"use strict";

function showExpenditureResults(result) {
    alert(result);
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

$("#expenditure-form").on("submit", submitExpenditure);