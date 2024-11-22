// Group the data by device_id
const groupedData = data.reduce((acc, item) => {
  if (!acc[item.device_id]) {
    acc[item.device_id] = { labels: [], values: [] };
  }
  acc[item.device_id].labels.push(
    new Date(item.timestamp * 1000).toISOString()
  ); // Convert timestamp to readable date
  acc[item.device_id].values.push(item.metric);
  return acc;
}, {});

console.log(groupedData);

const labels = data.map((item) => item.timestamp);
const values = data.map((item) => item.metric);

// Define simple color names for each line
const predefinedColors = ["blue", "green", "red", "yellow"];
const sortedKeys = Object.keys(groupedData).sort();
console.log(sortedKeys);

// Map each device to its own dataset with a predefined color
const datasets = Object.keys(groupedData).map((device_id, index) => ({
  label: device_id, // Name of the line
  data: groupedData[device_id].values, // Y-axis values
  borderColor: predefinedColors[index], // Use predefined color names
  backgroundColor: "transparent", // No background fill
  borderWidth: 2,
  tension: 0.4, // Smooth curves
}));

console.log(datasets);

const ctx = document.getElementById("lineChart").getContext("2d"); // Updated ID
const lineChart = new Chart(ctx, {
  type: "line",
  data: {
    labels: groupedData[Object.keys(groupedData)[0]].labels,
    datasets: datasets,
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        display: true,
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: "Timestamp",
        },
      },
      y: {
        title: {
          display: true,
          text: "Metric",
        },
        beginAtZero: true,
      },
    },
  },
});
