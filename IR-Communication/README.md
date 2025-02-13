<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IR Transmission</title>
    <script>
        function sendIR() {
            let message = document.getElementById("message").value;
            fetch('/send', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({"message": message})6
            }).then(response => response.json())
              .then(data => alert("Sent: " + data.message));
        }

        function receiveIR() {
            fetch('/receive')
            .then(response => response.json())
            .then(data => document.getElementById("received").innerText = "Received: " + data.received);
        }
    </script>
</head>
<body>
    <h1>IR Transmission Web Interface</h1>
    <label>Enter Message:</label>
    <input type="text" id="message" />
    <button onclick="sendIR()">Send</button>
    <br><br>
    <button onclick="receiveIR()">Receive</button>
    <p id="received">Received: </p>
</body>
</html># HTML
