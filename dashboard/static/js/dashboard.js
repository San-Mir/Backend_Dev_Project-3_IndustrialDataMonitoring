const socket = new WebSocket('ws://localhost:8000/ws/data/');

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log("Received data:", data);
    // You can now use `data` to update the frontend
};

