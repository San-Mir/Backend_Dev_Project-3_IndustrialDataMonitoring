const metricsContainer = document.getElementById("metrics");
const socket = new WebSocket(
  "ws://" + window.location.host + "/ws/sensor_data/"
);

socket.onmessage = function (event) {
  const data = JSON.parse(event.data);

  // Create a new metric entry with device info
  const metricElement = document.createElement("div");
  metricElement.className = "metric";
  metricElement.innerHTML = `<strong>Device:</strong> ${
    data.device_id
  } | <strong>Metric:</strong> ${
    data.metric
  } | <strong>Timestamp:</strong> ${new Date(
    data.timestamp * 1000
  ).toLocaleTimeString()}`;

  // Add the new metric to the top of the container
  metricsContainer.prepend(metricElement);

  // Optional: Limit displayed metrics to the latest 10
  if (metricsContainer.childElementCount > 10) {
    metricsContainer.removeChild(metricsContainer.lastChild);
  }
};
