// Obtenir une référence à l'élément de la fenêtre de chat et à l'entrée de chat
var chatWindow = document.querySelector('.chat-window');
var chatInput = document.getElementById('chat-input');
var messagesContainer = document.getElementById('chat-messages');

// Établir une connexion WebSocket
const socket = new WebSocket('ws://localhost:8080'); // Adresse de votre serveur WebSocket

// Fonction pour ajouter un message à la fenêtre de chat
function addMessage(message) {
    var messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.textContent = message;
    // chatWindow.appendChild(messageElement);
    messagesContainer.appendChild(messageElement);
    // Faire défiler vers le bas pour afficher le dernier message
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Gérer l'événement de soumission du formulaire de chat
document.getElementById('chat-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Empêcher le formulaire de se soumettre normalement
        var message = chatInput.value.trim(); // Obtenir le message de l'entrée de chat
        if (message !== '') {
            // Ajouter le message à la fenêtre de chat
            addMessage('You: ' + message);
            // Envoyer le message au serveur via WebSocket
            socket.send(JSON.stringify({ message: message }));
            // Effacer le champ de saisie après l'envoi du message
            chatInput.value = '';
        }
    }
});

// Recevoir les messages du serveur via WebSocket
socket.addEventListener('message', function(event) {
    var data = JSON.parse(event.data);
    var receivedMessage = data.message;
    // Ajouter le message reçu à la fenêtre de chat
    addMessage('Opponent: ' + receivedMessage);
});