"use strict";

function replaceBudget(results) {
    var budget = results;
    $('#budget-show').html(String(budget.budget) + budget.category);
    console.log(results)
    console.log("Finished replaceBudget");
}

function updateBudget(evt) {
    evt.preventDefault();

    var budget = $('#budget-form').serialize();

    $.post('/add-budget', budget, replaceBudget);
    console.log("Finished sending AJAX");
}

$('#budget-submit').click(updateBudget);