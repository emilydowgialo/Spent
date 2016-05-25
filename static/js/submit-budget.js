/* global $*/
"use strict";

function replaceBudget(results) {

    // Callback
    updateBudgetMinusExpenses(results);

    var budget = results;

    // Appends code for new expense
    var stringToAppend = '<form action="/remove-budget/' + String(budget.id) +
      '" method="POST" id="category-' + String(budget.category_id) + '">' +
      '<li>' +
      String(budget.budget) +
      '<br>' +
      String(budget.category) +
      '<br>' +
      '</li>' +
      '<input type="Submit" value="Remove">' +
      '</form>';

    console.log(stringToAppend);

    // This is the specific element
    var categoryElement = $('#category-' + String(budget.category_id));

    console.log(categoryElement);

    // If the element exists, replace with the new element
    if (categoryElement.length > 0) {
      categoryElement.replaceWith(stringToAppend);
    } else {
      $('#budget-div').append(stringToAppend);
      console.log(results);
      console.log("Finished replaceBudget");
    }
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

    // Gather info from the budget form
    var budget = $('#budget-form').serialize();

    // Parse form information, which returns information jsonified
    $.post('/add-budget', budget, replaceBudget);
    console.log("Finished sending AJAX");
}

// Submit button click event
$('#budget-submit').click(updateBudget);

