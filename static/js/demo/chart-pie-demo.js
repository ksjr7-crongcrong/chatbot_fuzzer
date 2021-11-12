// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
var ctx = document.getElementById("myPieChart");
let result = JSON.parse(document.getElementById("result_json"));
let level_count = [result.level_count.high, result.level_count.medium, result.level_count.low];
var level_count = document.getElementById("level_count").value.split("|");
var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ["위험", "주의"],
    datasets: [{
      data: level_count,
      backgroundColor: ['#db706c', '#fcf695'],
      hoverBackgroundColor: ['#db706c', '#fcf695'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});
