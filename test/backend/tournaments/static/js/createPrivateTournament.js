// Fichier create_tournament.js

// Ajoutez un écouteur d'événements lorsque le document est chargé
document.addEventListener('DOMContentLoaded', function() {
    // Ajoutez un écouteur d'événements pour soumettre le formulaire de création de tournoi
    document.getElementById('create-tournament-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Empêche la soumission par défaut du formulaire

        const tournamentName = document.getElementById('name').value;

        // Envoie d'une requête AJAX pour créer un tournoi
        fetch('/api/create_tournament/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({ name: tournamentName })
        })
        .then(response => {
            if (response.ok) {
                // Tournoi créé avec succès, redirection ou affichage d'un message de succès
                alert('Tournament created successfully!');
                window.location.href = '/tournament_list/'; // Redirige vers la page de liste des tournois
            } else {
                alert('Failed to create tournament. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again later.');
        });
    });
});
