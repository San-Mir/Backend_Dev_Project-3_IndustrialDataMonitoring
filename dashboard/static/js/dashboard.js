// Connect to WebSocket for real-time data updates
const socket = new WebSocket("ws://" + window.location.host + "/ws/monitor/");

socket.onmessage = function (event) {
  console.log("Received data:", event.data); // Log the incoming data to the console for debugging

  const data = JSON.parse(event.data);

  // Create a new div element to display the device data
  const dataContainer = document.getElementById("data-metrics");
  const deviceData = document.createElement("div");
  deviceData.classList.add("device-data");

  // Display device data
  deviceData.innerHTML = `
        <p><strong>Device ID:</strong> ${data.device_id}</p>
        <p><strong>Metric:</strong> ${data.metric}</p>
        <p><strong>Timestamp:</strong> ${new Date(
          data.timestamp * 1000
        ).toLocaleString()}</p>
    `;

  // Append the new data to the dashboard
  dataContainer.prepend(deviceData);
};

// Handle WebSocket errors
socket.onerror = function (error) {
  console.error("WebSocket error:", error);
};

// Close WebSocket connection on window unload
window.onbeforeunload = function () {
  socket.close();
};
