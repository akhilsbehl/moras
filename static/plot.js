function createChart(data, kanaType) {
  const processedData = data.filter(row => row['Kana Type'] === kanaType)
    .sort((a, b) => a.Accuracy - b.Accuracy);

  const labels = processedData.map(row => row.Kana);
  const accuracyData = processedData.map(row => row.Accuracy);
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
        label: 'Accuracy',
        data: accuracyData,
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }]
    },
    options: {
      indexAxis: 'y',
      plugins: {
        tooltip: {
          callbacks: {
            label: (context) => {
              const dataIndex = context.dataIndex;
              const timesSeen = timesSeenData[dataIndex];
              const timesCorrect = timesCorrectData[dataIndex];
              return `Accuracy: ${context.parsed.x.toFixed(2)} | Times Seen: ${timesSeen} | Times Correct: ${timesCorrect}`;
            }
          }
        }
      },
      scales: {
        x: {
          beginAtZero: true,
          max: 1
        }
      }
    }
  });
}

// Read the CSV file and process the data
Papa.parse('/static/analytics.csv', {
    header: true,
    download: true,
    complete: (results) => {
        const kanaTypes = Array.from(new Set(results.data.map(row => row['Kana Type'])));
        createChart(results.data, kanaTypes[0]);
        // Add toggle logic for Kana Types
        document.addEventListener('keydown', (event) => {
            if (event.key === 't') {
                const currentKanaType = kanaTypes.shift();
                kanaTypes.push(currentKanaType);
                createChart(results.data, kanaTypes[0]);
            }
        });
    }
});
