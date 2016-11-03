/* global $*/
"use strict";

function replaceBudget(results) {

    // Callback
    updateBudgetMinusExpenses(results);
    updateProgressBars(results);

    // The results budget
    var budget = results;

    // This is the category at hand
    var stringToAppend = String(budget.budget);

    // This is the element to edit
    var budgetElement = $('#budget-' + String(budget.category_id));

  // Appends the info to the element
  budgetElement.html(stringToAppend);
  console.log("finished replaceBudget");
}

function updateProgressBars(results) {

    // This contains info about the new budget
    var progBarInfo = results;

    console.log("this is progbarinfo");
    console.log(progBarInfo);

    // These are the elements on dashboard.html we want to change
    var divInfo = $('#progbar-' + String(progBarInfo.category_id));
    var progNum = $('#prognum-' + String(progBarInfo.category_id));

    console.log("this is prognum and progbar");
    console.log(progNum);
    console.log(divInfo);

    // Target the elements on dashboard.html
    divInfo.css( "width", String(progBarInfo.category_progress) + "%" );
    progNum.html("$" + String(progBarInfo.cat_budget_minus_expenses));
}

function updateBudgetMinusExpenses(resp) {

  // The results budget
  var budget = resp;

  // This is the category at hand
  var stringToAppend = String(budget.cat_budget_minus_expenses);

  // This is the element to edit
  var budgetElement = $('#budget-left-' + String(budget.category_id));

  // Appends the info to the element
  budgetElement.html(stringToAppend);
  console.log("finished updateBudgetMinusExpenses");

}

function updateBudget(evt) {
    evt.preventDefault();

    window.Intercom('update');

    // Close the modal via Javascript when the event is triggered
    $('#addBudget').modal('toggle');

    // Gather info from the budget form
    var budget = $('#budget-form').serialize();

    // Parse form information, which returns information jsonified
    $.post('/add-budget', budget, replaceBudget);
    console.log("Finished sending AJAX");
}

// Submit button click event
$('#budget-submit').click(updateBudget);
