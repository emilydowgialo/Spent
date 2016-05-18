"use strict";

function showBudgetResults(result) {
    alert(result);
}

function submitBudget(evt) {
    evt.preventDefault();

    var formInputs = {
        "category": $("#category-field").val(),
        "budget": $("#budget").val()
    };

    $.post("/add-budget", 
           formInputs,
           showBudgetResults
           );
}

$("#budget-form").on("submit", submitBudget);