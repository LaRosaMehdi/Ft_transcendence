// Fichier join_tournament.js

// Ajoutez un écouteur d'événements lorsque le document est chargé
document.addEventListener('DOMContentLoaded', function() {
    // Ajoutez un écouteur d'événements pour soumettre le formulaire de rejoindre un tournoi
    document.getElementById('join-tournament-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Empêche la soumission par défaut du formulaire

        const playerName = document.getElementById('player-name').value;
        const tournamentId = document.getElementById('tournament-id').value;

        // Envoie d'une requête AJAX pour rejoindre un tournoi
        fetch('/api/join_tournament/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({ player_name: playerName, tournament_id: tournamentId })
        })
        .then(response => {
            if (response.ok) {
                // Joueur rejoint le tournoi avec succès, redirection ou affichage d'un message de succès
                alert('You\'ve successfully joined the tournament!');
                // Redirection vers une page de confirmation ou une autre page appropriée
            } else {
                alert('Failed to join tournament. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again later.');
        });
    });
});
