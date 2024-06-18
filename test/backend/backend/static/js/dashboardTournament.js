function tournamentLaunchGame() {
    const tournamentName = window.tournamentName;
    if (!tournamentName) {
        console.log("Tournament name is not set");
        return;
    }
    fetch(`/tournaments/${tournamentName}/launch/`)
        .then(response => {
            if (response.redirected) {
                const path = new URL(response.url).pathname.replace('/tournaments/', '');
                loadPageTournament(path);
            }
            else
                console.log("Nothing change")
        })
        .catch(error => console.error('Error:', error));
}

function fetchTournamentDetails() {
    const tournamentName = window.tournamentName;
    if (!tournamentName) {
        console.log("Tournament name is not set");
        return;
    }

    fetch(`/tournaments/${tournamentName}/get/`)
        .then(response => response.json())
        .then(data => {
            renderName(data.name);
            renderLevel(data.level);
            renderNbPlayers(data.nb_players);
            renderPlayersRanking(data.players);
            renderGames(data.games);
        })
        .catch(error => console.error('Failed to fetch tournament details', error));
}

function renderName(name) {
    const nameContainer = document.getElementById('tournament-name');
    if (nameContainer) {
        nameContainer.innerHTML = `<h1>Tournament ${name}</h1>`;
    }
}

function renderLevel(level) {
    const levelContainer = document.getElementById('tournament-level');
    if (levelContainer) {
        levelContainer.innerHTML = `<h4>Currently playing for the ${level}</h4>`;
    }
}

function renderNbPlayers(nbPlayers) {
    const nbPlayersContainer = document.getElementById('tournament-nb-players');
    if (nbPlayersContainer) {
        nbPlayersContainer.innerHTML = `<h4>${nbPlayers} player tournament</h4>`;
    }
}

function renderPlayersRanking(players) {
    const playersListContainer = document.getElementById('tournament-ranking');
    if (playersListContainer) {
        let playersListHTML = '<div class="dashboard-ranking"><h2>Players Ranking</h2><div class="players-container">';

        players.forEach((player, index) => {
            playersListHTML += `
                <div class="player-item">
                    <h6 class="rank">${player.rank}</h6>
                    <img src="${player.image}" alt="${player.username}">
                    <p>${player.username} aka ${player.alias}</p>
                </div>
            `;
            if (index === players.length - 1 && players.length % 2 !== 0) {
                playersListHTML += '<div class="player-item"></div>'; // Add an empty item to force the last player into a single column
            }
        });

        playersListHTML += '</div></div>';
        playersListContainer.innerHTML = playersListHTML;
    }
}

function renderGames(games) {
    const gamesListContainer = document.getElementById('tournament-games');
    if (gamesListContainer) {
        if (games.length == 0) {
            gamesListContainer.innerHTML = `
                <div>
                    <h2>Upcoming Games</h2>
                    <p>Tournament finished, no more games to play!</p>
                </div>
            `;
        } else {
            gamesListContainer.innerHTML = `
                <div>
                    <h2>Upcoming Games</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Level</th>
                                <th>Player 1</th>
                                <th>Player 2</th>
                                <th>State</th>
                                <th>Score</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${games.map(game => `
                                <tr>
                                    <td>${game.level}</td>
                                    <td>${game.player1}</td>
                                    <td>${game.player2}</td>
                                    <td>${game.state}</td>
                                    <td>${game.score}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            `;
        }
    }
}

function initTournamentPage() {
    const tournamentElement = document.getElementById('tournament-name');
    if (!tournamentElement) {
        console.log('Tournament name element not found');
        return;
    }

    window.tournamentName = tournamentElement.dataset.tournamentName;
    if (!window.tournamentName) {
        console.log("Tournament name is not set in the dataset");
        return;
    }

    fetchTournamentDetails();
    setInterval(fetchTournamentDetails, 5000);
    tournamentLaunchGame();
    setInterval(tournamentLaunchGame, 10000);
}


