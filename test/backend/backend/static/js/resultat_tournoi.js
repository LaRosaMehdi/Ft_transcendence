document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('player-form');
    var tableBody = document.getElementById('results-body');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        tableBody.innerHTML = ''; // Effacer le contenu précédent
        var numPlayers = parseInt(document.getElementById('num-players').value, 10);
        console.log("Nombre de joueurs à générer :", numPlayers);

        // Générer les lignes du tableau pour chaque joueur
        for (var i = 0; i < numPlayers; i++) {
            var player = {
                position: i + 1,
                name: 'Player ' + (i + 1),
                wins: Math.floor(Math.random() * 10),
                draws: Math.floor(Math.random() * 5),
                losses: Math.floor(Math.random() * 5)
            };
            console.log("Joueur à ajouter :", player);
            var row = document.createElement('tr');
            row.innerHTML = `
                <td>${player.position}</td>
                <td>${player.name}</td>
                <td>${player.wins}</td>
                <td>${player.draws}</td>
                <td>${player.losses}</td>
            `;
            
            console.log("Ligne du tableau :", row.innerHTML);
            tableBody.appendChild(row);
        }
    });
});