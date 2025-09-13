const socket = io();

socket.on('connect', () => {
    console.log('Connected to server');
});

socket.on('receive_message', (data) => {
    const chatBox = document.getElementById('chat-box');
    const newMsg = document.createElement('p');
    newMsg.innerHTML = `<strong>${data.username}</strong>: ${data.message}`;
    chatBox.appendChild(newMsg);
    chatBox.scrollTop = chatBox.scrollHeight;
});

function sendMessage() {
    const input = document.getElementById('message-input');
    const msg = input.value;
    if (msg.trim() !== "") {
        const username = document.body.getAttribute('data-username');
        socket.emit('send_message', { username: username, message: msg });
        input.value = "";
    }
}
