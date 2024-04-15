// Établir une connexion WebSocket avec le serveur de matchmaking
const socket = new WebSocket('ws://adresse_du_serveur:port');

// Lorsque la connexion WebSocket est ouverte
socket.onopen = function() {
    console.log('Connexion WebSocket établie avec le serveur.');
};

// Lorsque le joueur clique sur le bouton "Play"
document.getElementById('play-button').addEventListener('click', function() {
    // Envoyer une demande de matchmaking au serveur
    socket.send(JSON.stringify({ action: 'requestMatchmaking' }));
});

// Gérer les messages provenant du serveur
socket.onmessage = function(event) {
    const message = JSON.parse(event.data);
    // Si le serveur envoie une notification de match
    if (message.action === 'matchFound') {
        // Extraire les informations du message de match
        const opponentInfo = message.opponentInfo;
        // Afficher une notification de match trouvée
        alert('Match trouvé avec : ' + opponentInfo.username);
        // Vous pouvez également démarrer le jeu ici
    }
};
