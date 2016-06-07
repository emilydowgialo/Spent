
// Charts are from chart.js

function charts() {

  var options = {
    responsive: true
  };

  var ctx_donut = $("#donutChart").get(0).getContext("2d");

  // Gets info from this route in server.py and sends to the donut chart
  $.get("/expenditure-types.json", function (data) {
    var myDonutChart = new Chart(ctx_donut).Doughnut(data.expenditures, options);
    $('#donutLegend').html(myDonutChart.generateLegend());
  });

  var ctx_line = $("#barChart").get(0).getContext("2d");

  // Gets info from this route in server.py and sends to the bar chart
  $.get("/total-spent.json", function (data) {
    var myBarChart = new Chart(ctx_line).Bar(data, options);
    $("#BarLegend").html(myBarChart.generateLegend());
  });

}

// Call the function so the charts display upon page load
charts();