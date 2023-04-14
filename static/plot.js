function createChart(data, kanaType) {
  const processedData = data.filter(row => row['Kana Type'] === kanaType)
    .sort((a, b) => a.Accuracy - b.Accuracy);

  const labels = processedData.map(row => row.Kana);
  const accuracyData = processedData.map(row => row.Accuracy * 100); // Convert to percentage
  const timesSeenData = processedData.map(row => row['Times Seen']);
  const timesCorrectData = processedData.map(row => row['Times Correct']);

  const ctx = document.getElementById('myChart').getContext('2d');
  
  // Destroy the previous chart if it exists
  if (window.myChart && window.myChart.destroy) {
    window.myChart.destroy();
  }

  window.myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        data: accuracyData,
        backgroundColor: 'rgba(255, 206, 86, 0.2)', // Light yellowish color
        borderColor: 'rgba(255, 206, 86, 1)',
        borderWidth: 1,
        barPercentage: 0.5
      }]
    },
    options: {
      plugins: {
        title: {
          display: false // Remove the title
        },
        tooltip: {
          callbacks: {
            label: (context) => {
              const dataIndex = context.dataIndex;
              const timesSeen = timesSeenData[dataIndex];
              const timesCorrect = timesCorrectData[dataIndex];
              return `Accuracy: ${context.parsed.y.toFixed(2)}% | Times Seen: ${timesSeen} | Times Correct: ${timesCorrect}`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 100 // Change the scale to 0 - 100
        }
      },
      responsive: true,
      maintainAspectRatio: true,
      barValueSpacing: 20
    }
  });
}

function updateChart() {
  const kanaType = document.querySelector('input[name="kanaType"]:checked').value;
  createChart(window.csvData, kanaType);
}

Papa.parse('static/analytics.csv', {
    download:true,
    header: true,
    dynamicTyping: true,
    skipEmptyLines: true,
    complete: (results) => {
        window.csvData = results.data;
        updateChart();
    }
});
function createChart(data, kanaType) {
  const processedData = data.filter(row => row['Kana Type'] === kanaType)
    .sort((a, b) => a.Accuracy - b.Accuracy);

  const labels = processedData.map(row => row.Kana);
  const accuracyData = processedData.map(row => row.Accuracy * 100); // Convert to percentage
  const timesSeenData = processedData.map(row => row['Times Seen']);
  const timesCorrectData = processedData.map(row => row['Times Correct']);

  const ctx = document.getElementById('myChart').getContext('2d');
  
  // Destroy the previous chart if it exists
  if (window.myChart && window.myChart.destroy) {
    window.myChart.destroy();
  }

  window.myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        data: accuracyData,
        backgroundColor: '#133955', // Fill color
        borderColor: '#286038', // Border color
        borderWidth: 1
      }]
    },
    options: {
      plugins: {
        legend: {
          display: false // Remove the legend
        },
        tooltip: {
          callbacks: {
            label: (context) => {
              const dataIndex = context.dataIndex;
              const timesSeen = timesSeenData[dataIndex];
              const timesCorrect = timesCorrectData[dataIndex];
              return `Accuracy: ${context.parsed.y.toFixed(2)}% | Times Seen: ${timesSeen} | Times Correct: ${timesCorrect}`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 100 // Change the scale to 0 - 100
        },
        x: {
          categoryPercentage: 0.5, // Adjust the width of the bars
          barPercentage: 1
        }
      },
      responsive: true,
      maintainAspectRatio: true,
    }
  });
}

function updateChart() {
  const kanaType = document.querySelector('input[name="kanaType"]:checked').value;
  createChart(window.csvData, kanaType);
}

Papa.parse('static/analytics.csv', {
    download:true,
    header: true,
    dynamicTyping: true,
    skipEmptyLines: true,
    complete: (results) => {
        window.csvData = results.data;
        updateChart();
    }
});
