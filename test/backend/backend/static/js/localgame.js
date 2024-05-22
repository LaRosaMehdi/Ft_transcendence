document.addEventListener('DOMContentLoaded', function() {
    var scriptTag = document.querySelector('script[src*="localgame.js"]');
    var csrfToken = scriptTag.getAttribute('value');

    console.log(csrfToken);

    const canvas = document.getElementById('pongCanvas');
    const ctx = canvas.getContext('2d');

    const player1 = {
        x: 50,
        y: canvas.height / 2 - 50,
        width: canvas.width / 50,
        height: canvas.height / 3,
        color: 'blue',
        speed: 5,
        keys: ['ArrowUp', 'ArrowDown'] // Touches pour le joueur 1
    };
    
    const player2 = {
        x: canvas.width - 60,
        y: canvas.height / 2 - 50,
        width: canvas.width / 50,
        height: canvas.height / 3,
        color: 'red',
        speed: 5,
        keys: ['w', 's'] // Touches pour le joueur 2
    };
    
    const keysPressed = {
        'ArrowUp': false,
        'ArrowDown': false,
        'w': false,
        's': false
    };


    let scorePlayer1 = 0; // Ajout de la variable scorePlayer1
    let scorePlayer2 = 0; // Ajout de la variable scorePlayer2
    // Dessiner les plateformes des joueurs
    function drawPlayers() {
        ctx.fillStyle = player1.color;
        ctx.fillRect(player1.x, player1.y, player1.width, player1.height);
    
        ctx.fillStyle = player2.color;
        ctx.fillRect(player2.x, player2.y, player2.width, player2.height);
    }
    
    // Gestion de la sélection du joueur
    let player1Chosen = false;
    let player2Chosen = false;
    
    function choosePlayer(player) {
        if (player === 'player1') {
            player1Chosen = true;
            if (!player1Chosen) {
            } else {
                return;
            }
        } else if (player === 'player2') {
            if (!player2Chosen) {
                player2Chosen = true;
            } else {
                return;
            }
        }
    
        console.log('Player selected:', player);
        if (player1Chosen && player2Chosen) {
            canvas.style.visibility = 'visible';
            startGame(); // Démarrer le jeu lorsque les deux joueurs ont choisi leur plateforme
        }
    }

    document.getElementById('play-btn').addEventListener('click', function() {
        canvas.style.visibility = 'visible';
        startGame();
    });
    
    document.getElementById('player1-btn').addEventListener('click', function() {
        choosePlayer('player1');
    });
    
    document.getElementById('player2-btn').addEventListener('click', function() {
        choosePlayer('player2');
    });
    
    function handleKeyEvents(event) {
        if (player1.keys.includes(event.key)) {
            event.preventDefault();
            if (event.key === player1.keys[0] && player1.y > 0) {
                player1.y -= player1.speed; // Déplacer le joueur 1 vers le haut
            } else if (event.key === player1.keys[1] && player1.y + player1.height < canvas.height) {
                player1.y += player1.speed; // Déplacer le joueur 1 vers le bas
            }
        }
    
        if (player2.keys.includes(event.key)) {
            event.preventDefault();
            if (event.key === player2.keys[0] && player2.y > 0) {
                player2.y -= player2.speed; // Déplacer le joueur 2 vers le haut
            } else if (event.key === player2.keys[1] && player2.y + player2.height < canvas.height) {
                player2.y += player2.speed; // Déplacer le joueur 2 vers le bas
            }
        }
    }
    
    document.addEventListener('keydown', handleKeyEvents);
    
    function handleKeyDown(event) {
        if (keysPressed.hasOwnProperty(event.key)) {
            keysPressed[event.key] = true;
        }
    }
    
    function handleKeyUp(event) {
        if (keysPressed.hasOwnProperty(event.key)) {
            keysPressed[event.key] = false;
        }
    }
    
    document.addEventListener('keydown', handleKeyDown);
    document.addEventListener('keyup', handleKeyUp);

    function movePlayers() {
        if (keysPressed['ArrowUp'] && player1.y > 0) {
            player1.y -= player1.speed;
        }
        if (keysPressed['ArrowDown'] && player1.y + player1.height < canvas.height) {
            player1.y += player1.speed;
        }
        if (keysPressed['w'] && player2.y > 0) {
            player2.y -= player2.speed;
        }
        if (keysPressed['s'] && player2.y + player2.height < canvas.height) {
            player2.y += player2.speed;
        }
    }

    const accelerationRate = 0.1; 
    const baseBallSpeed = 1; // Vitesse de base de la balle
    let currentBallSpeed = baseBallSpeed; // Vitesse actuelle de la balle
    
    const ball = {
        x: canvas.width / 2,
        y: canvas.height / 2,
        radius: 10,
        dx: 2,
        dy: -2
    };
    
    function drawBall() {
        ctx.beginPath();
        ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
        ctx.fillStyle = 'red';
        ctx.fill();
        ctx.closePath();
    }


    function stopBall() {
        // Arrêter le mouvement de la balle
        ball.dx = 0;
        ball.dy = 0;
    }


    function resetBall() {
        ball.x = canvas.width / 2;
        ball.y = canvas.height / 2;
        ball.dx = -ball.dx; // Changement de direction de la balle après chaque point marqué
        ball.dy = -ball.dy;
        currentBallSpeed = baseBallSpeed;
        ball.dx = Math.sign(ball.dx) * baseBallSpeed;
        ball.dy = Math.sign(ball.dy) * baseBallSpeed;
        player1.y = canvas.height / 2 - 50;
        player2.y = canvas.height / 2 - 50;    
    }

    function handleCollision() {
        if (ball.y - ball.radius <= 0 || ball.y + ball.radius >= canvas.height) {
            ball.dy = -ball.dy; // Inverser la direction verticale de la balle
        }
        // Gestion de la collision ici
        if (ball.x - ball.radius <= 1) {
            // La balle a atteint le mur gauche, le joueur 2 marque un point
            scorePlayer2++;
            resetBall(); // Réinitialiser la position de la balle
            return; // Sortir de la fonction après la gestion de la collision
        }
        if (ball.x + ball.radius >= canvas.width - 1) {
            // La balle a atteint le mur droit, le joueur 1 marque un point
            scorePlayer1++;
            resetBall(); // Réinitialiser la position de la balle
            return; // Sortir de la fonction après la gestion de la collision
        }
        // Collision avec le joueur 1   
        if (ball.x - ball.radius <= player1.x + player1.width &&
        ball.x - ball.radius >= player1.x &&
        ball.y + ball.radius >= player1.y &&
        ball.y - ball.radius <= player1.y + player1.height) {
        ball.dx = -ball.dx; // Inverser la direction horizontale de la balle
        currentBallSpeed += accelerationRate;
        ball.x = player1.x + player1.width + ball.radius;
         }

        // Vérifier la collision avec le joueur 2
        if (ball.x + ball.radius >= player2.x &&
            ball.x + ball.radius <= player2.x + player2.width &&
            ball.y + ball.radius >= player2.y &&
            ball.y - ball.radius <= player2.y + player2.height) {
            ball.dx = -ball.dx; // Inverser la direction horizontale de la balle
            currentBallSpeed += accelerationRate;
            ball.x = player2.x - ball.radius;
        }
    }

    function drawScores() {
        // Dessiner les scores ici
        ctx.font = '24px Arial';
        ctx.fillStyle = 'white';
        ctx.fillText('Player 1: ' + scorePlayer1, 20, 30);
        ctx.fillText('Player 2: ' + scorePlayer2, canvas.width - 150, 30);
    }


    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = 'black'; // Remplacez 'blue' par la couleur de votre choix
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.beginPath();
        ctx.strokeStyle = 'white';
        ctx.lineWidth = 2;
        ctx.moveTo(canvas.width / 2, 0);
        ctx.lineTo(canvas.width / 2, canvas.height);
        ctx.stroke();
        drawPlayers();
        drawBall();
        drawScores();
        movePlayers();
        handleCollision();
        ball.dx += accelerationRate * Math.sign(ball.dx);
        ball.dy += accelerationRate * Math.sign(ball.dy);

        ball.x += ball.dx; // Appliquer la vitesse actuelle de la balle
        ball.y += ball.dy;
        requestAnimationFrame(draw);
    }

    
    function endGame(game) {
        const player1Score = scorePlayer1;
        const player2Score = scorePlayer2;

        const obj = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                player1_score: player1Score,
                player2_score: player2Score,
            }),
        }



        console.log(obj);
        console.log(document.cookie);


        fetch('/games/finishAndquit/', obj)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Game finished successfully:', data);
            // Rediriger vers la page des résultats
            window.location.href = '/games/results/';
        })
        .catch(error => {
            console.error('Error:', error);
        });
        let winner, loser;
        if (scorePlayer1 > scorePlayer2) {
            winner = "Joueur 1";
            loser = "Joueur 2";
        } else if (scorePlayer2 > scorePlayer1) {
            winner = "Joueur 2";
            loser = "Joueur 1";
        } else {
            winner = "Personne (égalité)";
            loser = "Personne (égalité)";
        }
        alert(`Le temps est écoulé! ${winner} remporte la partie avec ${Math.max(scorePlayer1, scorePlayer2)} points contre ${loser} avec ${Math.min(scorePlayer1, scorePlayer2)} points.`);
        resetBall();
        stopBall();
        // window.location.href = '/games/game_update/';
    }


    let countdownInterval; // Déclaration d'une variable globale pour stocker l'identifiant de l'intervalle du compte à rebours

function startTimer(durationInSeconds) {
    let timer = durationInSeconds; // Durée initiale du chronomètre en secondes

    // Fonction qui met à jour le chrono et l'affiche
    function updateTimer() {
        const minutes = Math.floor(timer / 60);
        let seconds = timer % 60;

        // Ajout d'un zéro devant le nombre si les secondes sont inférieures à 10
        seconds = seconds < 10 ? '0' + seconds : seconds;

        // Affichage du chrono
        document.getElementById('chrono-button').textContent = minutes + ':' + seconds;

        // Décrémentation du chrono
        if (timer-- <= 0) {
            clearInterval(countdownInterval); // Arrêter le compte à rebours lorsque le temps est écoulé
            endGame();
            // alert('Time is up!'); // Afficher un message lorsque le temps est écoulé (vous pouvez modifier cela selon vos besoins)
        }
    }

    // Appel de la fonction updateTimer toutes les secondes
        updateTimer();
        countdownInterval = setInterval(updateTimer, 1000); // Mettre à jour le chrono toutes les 1000 ms (1 seconde)
    }

    function startGame() {
        startTimer(7);
        draw();
    }
});


/* document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('pongCanvas');
    const ctx = canvas.getContext('2d');
        const player1 = {
            x: 50,
            y: canvas.height / 2 - 50,
            width: canvas.width / 50,
            height: canvas.height / 3,
            color: 'blue',
            speed: 5,
            keys: ['ArrowUp', 'ArrowDown'] // Touches pour le joueur 1
        };

        const player2 = {
            x: canvas.width - 60,
            y: canvas.height / 2 - 50,
            width: canvas.width / 50,
            height: canvas.height / 3,
            color: 'red',
            speed: 5,
            keys: ['w', 's'] // Touches pour le joueur 2
        };    

        const keysPressed = {
            'ArrowUp': false,
            'ArrowDown': false,
            'w': false,
            's': false
        };    

        const ball = {
            x: canvas.width / 2,
            y: canvas.height / 2,
            radius: 10,
            dx: 2,
            dy: -2
        };    


        const playerButtons = document.querySelectorAll('.player-button');
        let role;


        playerButtons.forEach(button => {
           button.addEventListener('click', function() {
            role = button.getAttribute('data-role'); // Définir le rôle lorsque le bouton est cliqué   
            choosePlayer(role);
            });
        });

        function drawHostCanvas() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawPlayers();
            drawBall();
            drawScores();
            movePlayers();
            handleCollision();
            ball.dx += accelerationRate * Math.sign(ball.dx);
            ball.dy += accelerationRate * Math.sign(ball.dy);
            ball.x += ball.dx; // Appliquer la vitesse actuelle de la balle
            ball.y += ball.dy;
        }

        function sendGameStateToServer() {
        fetch('/update_game_state/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + YOUR_JWT_TOKEN // Remplacez YOUR_JWT_TOKEN par votre token JWT si nécessaire
            },    
            body: JSON.stringify({
                // Envoyez ici l'état actuel du jeu, par exemple les positions des joueurs et de la balle
                player1: {
                    x: player1.x,
                    y: player1.y,
                    // Ajoutez d'autres propriétés si nécessaire
                },    
                player2: {
                    x: player2.x,
                    y: player2.y,
                    // Ajoutez d'autres propriétés si nécessaire
                },    
                ball: {
                    x: ball.x,
                    y: ball.y,
                    // Ajoutez d'autres propriétés si nécessaire
                }    
            }),    
        })    
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }    
        })    
        .catch(error => console.error('Error:', error));
    }
    
    
    
    function drawSpectatorPlayer(x, y, color, width, height) {
        ctx.fillStyle = color;
        ctx.fillRect(x, y, width, height);
    }    
    
    
    function drawSpectatorBall(x, y, color, radius) {
            ctx.beginPath();
            ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
            ctx.fillStyle = 'red';
            ctx.fill();
            ctx.closePath();
    }
    
    function drawSpectatorCanvas(data) {
        // Effacer le canvas du spectateur
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    
        ctx.fillStyle = 'black'; // Remplacez 'blue' par la couleur de votre choix
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.beginPath();
        ctx.strokeStyle = 'white';
        ctx.lineWidth = 2;
        ctx.moveTo(canvas.width / 2, 0);
        ctx.lineTo(canvas.width / 2, canvas.height);
        ctx.stroke();
        drawSpectatorPlayer(data.player1.x, data.player1.y, data.player1.color, data.player1.width, data.player1.height);
        drawSpectatorPlayer(data.player2.x, data.player2.y, data.player2.color, data.player1.width, data.player1.height);
        drawSpectatorBall(data.ball.x, data.ball.y, data.ball.color, data.ball.radius);
        drawScores();
        movePlayers();
        handleCollision();
        ball.dx += accelerationRate * Math.sign(ball.dx);
        ball.dy += accelerationRate * Math.sign(ball.dy);
    
        ball.x += ball.dx; // Appliquer la vitesse actuelle de la balle
        ball.y += ball.dy;
        requestAnimationFrame(draw);
        // Dessiner les éléments du canvas du joueur hôte sur le canvas du spectateur
        // Exemple : drawPlayer(data.player1Position.x, data.player1Position.y);
        // Exemple : drawPlayer(data.player2Position.x, data.player2Position.y);
        // Exemple : drawBall(data.ballPosition.x, data.ballPosition.y);
    }
    
    function updateSpectatorCanvas() {
            // Effectuer une requête AJAX pour récupérer les données du canvas du joueur hôte
        fetch('/get_game_state/')
            .then(response => response.json())
            .then(data => {
                // Dessiner les données récupérées sur le canvas du spectateur
                drawSpectatorCanvas(data);
            })
            .catch(error => console.error('Error:', error));
    }
    
    


    let scorePlayer1 = 0; // Ajout de la variable scorePlayer1
    let scorePlayer2 = 0; // Ajout de la variable scorePlayer2
    // Dessiner les plateformes des joueurs
    function drawPlayers() {
        ctx.fillStyle = player1.color;
        ctx.fillRect(player1.x, player1.y, player1.width, player1.height);
    
        ctx.fillStyle = player2.color;
        ctx.fillRect(player2.x, player2.y, player2.width, player2.height);
    }
    
    // Gestion de la sélection du joueur
    let player1Chosen = false;
    let player2Chosen = false;
    
    function choosePlayer(player) {
        const role = player.getAttribute('data-role');
        if (role === 'host' || role === 'spectator') {
            // Logique pour l'hôte
            sendGameStateToServer();
        } else if (player === 'spectator') {
            setInterval(updateSpectatorCanvas, 1000);
            // Logique pour le spectateur
        }
        if (player === 'player1') {
            if (!player1Chosen) {
                player1Chosen = true;
            } else {
                alert('Plateforme déjà sélectionnée par le joueur 1.');
                return;
            }
        } else if (player === 'player2') {
            if (!player2Chosen) {
                player2Chosen = true;
            } else {
                alert('Plateforme déjà sélectionnée par le joueur 2.');
                return;
            }
        }
    
        console.log('Player selected:', player);
        if (player1Chosen && player2Chosen) {
            canvas.style.visibility = 'visible';
            startGame(); // Démarrer le jeu lorsque les deux joueurs ont choisi leur plateforme
        }
        if (role === 'spectator') {
        canvas.style.visibility = 'visible';
        startGame();
    }
    }
    
    document.getElementById('player1-btn').addEventListener('click', function() {
        choosePlayer(this);
    });
    
    document.getElementById('player2-btn').addEventListener('click', function() {
        choosePlayer(this);
    });
    
    function handleKeyEvents(event) {
        if (player1.keys.includes(event.key)) {
            event.preventDefault();
            if (event.key === player1.keys[0] && player1.y > 0) {
                player1.y -= player1.speed; // Déplacer le joueur 1 vers le haut
            } else if (event.key === player1.keys[1] && player1.y + player1.height < canvas.height) {
                player1.y += player1.speed; // Déplacer le joueur 1 vers le bas
            }
        }
    
        if (player2.keys.includes(event.key)) {
            event.preventDefault();
            if (event.key === player2.keys[0] && player2.y > 0) {
                player2.y -= player2.speed; // Déplacer le joueur 2 vers le haut
            } else if (event.key === player2.keys[1] && player2.y + player2.height < canvas.height) {
                player2.y += player2.speed; // Déplacer le joueur 2 vers le bas
            }
        }
    }
    
    document.addEventListener('keydown', handleKeyEvents);
    
    function handleKeyDown(event) {
        if (keysPressed.hasOwnProperty(event.key)) {
            keysPressed[event.key] = true;
        }
    }
    
    function handleKeyUp(event) {
        if (keysPressed.hasOwnProperty(event.key)) {
            keysPressed[event.key] = false;
        }
    }
    
    document.addEventListener('keydown', handleKeyDown);
    document.addEventListener('keyup', handleKeyUp);

    function movePlayers() {
        if (keysPressed['ArrowUp'] && player1.y > 0) {
            player1.y -= player1.speed;
        }
        if (keysPressed['ArrowDown'] && player1.y + player1.height < canvas.height) {
            player1.y += player1.speed;
        }
        if (keysPressed['w'] && player2.y > 0) {
            player2.y -= player2.speed;
        }
        if (keysPressed['s'] && player2.y + player2.height < canvas.height) {
            player2.y += player2.speed;
        }
    }

    const accelerationRate = 0.005; 
    const baseBallSpeed = 1; // Vitesse de base de la balle
    let currentBallSpeed = baseBallSpeed; // Vitesse actuelle de la balle
    
  
    function drawBall() {
        ctx.beginPath();
        ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
        ctx.fillStyle = 'red';
        ctx.fill();
        ctx.closePath();
    }


    function stopBall() {
        // Arrêter le mouvement de la balle
        ball.dx = 0;
        ball.dy = 0;
    }


    function resetBall() {
        ball.x = canvas.width / 2;
        ball.y = canvas.height / 2;
        ball.dx = -ball.dx; // Changement de direction de la balle après chaque point marqué
        ball.dy = -ball.dy;
        currentBallSpeed = baseBallSpeed;
        ball.dx = Math.sign(ball.dx) * baseBallSpeed;
        ball.dy = Math.sign(ball.dy) * baseBallSpeed;
        player1.y = canvas.height / 2 - 50;
        player2.y = canvas.height / 2 - 50;    }

    function handleCollision() {
        if (ball.y - ball.radius <= 0 || ball.y + ball.radius >= canvas.height) {
            ball.dy = -ball.dy; // Inverser la direction verticale de la balle
        }
        // Gestion de la collision ici
        if (ball.x - ball.radius <= 1) {
            // La balle a atteint le mur gauche, le joueur 2 marque un point
            scorePlayer2++;
            resetBall(); // Réinitialiser la position de la balle
            return; // Sortir de la fonction après la gestion de la collision
        }
        if (ball.x + ball.radius >= canvas.width - 1) {
            // La balle a atteint le mur droit, le joueur 1 marque un point
            scorePlayer1++;
            resetBall(); // Réinitialiser la position de la balle
            return; // Sortir de la fonction après la gestion de la collision
        }
        // Collision avec le joueur 1   
        if (ball.x - ball.radius <= player1.x + player1.width &&
            ball.y >= player1.y && ball.y <= player1.y + player1.height) {
            ball.dx = -ball.dx; // Inverser la direction horizontale de la balle
            currentBallSpeed += accelerationRate;
        }
    
        // Vérifier la collision avec le joueur 2
        if (ball.x + ball.radius >= player2.x &&
            ball.y >= player2.y && ball.y <= player2.y + player2.height) {
            ball.dx = -ball.dx; // Inverser la direction horizontale de la balle
            currentBallSpeed += accelerationRate;
        }
    }

    function drawScores() {
        // Dessiner les scores ici
        ctx.font = '24px Arial';
        ctx.fillStyle = 'white';
        ctx.fillText('Player 1: ' + scorePlayer1, 20, 30);
        ctx.fillText('Player 2: ' + scorePlayer2, canvas.width - 150, 30);
    }


    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = 'black'; // Remplacez 'blue' par la couleur de votre choix
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.beginPath();
        ctx.strokeStyle = 'white';
        ctx.lineWidth = 2;
        ctx.moveTo(canvas.width / 2, 0);
        ctx.lineTo(canvas.width / 2, canvas.height);
        ctx.stroke();
        drawPlayers();
        drawBall();
        drawScores();
        movePlayers();
        handleCollision();
        ball.dx += accelerationRate * Math.sign(ball.dx);
        ball.dy += accelerationRate * Math.sign(ball.dy);

        ball.x += ball.dx; // Appliquer la vitesse actuelle de la balle
        ball.y += ball.dy;
        requestAnimationFrame(draw);
    }


    function endGame() {
        // Afficher le gagnant et le perdant en fonction du score
        let winner, loser;
        if (scorePlayer1 > scorePlayer2) {
            winner = "Joueur 1";
            loser = "Joueur 2";
        } else if (scorePlayer2 > scorePlayer1) {
            winner = "Joueur 2";
            loser = "Joueur 1";
        } else {
            winner = "Personne (égalité)";
            loser = "Personne (égalité)";
        }
        alert(`Le temps est écoulé! ${winner} remporte la partie avec ${Math.max(scorePlayer1, scorePlayer2)} points contre ${loser} avec ${Math.min(scorePlayer1, scorePlayer2)} points.`);
        resetBall();
        stopBall();
    }

    let countdownInterval; // Déclaration d'une variable globale pour stocker l'identifiant de l'intervalle du compte à rebours

function startTimer(durationInSeconds) {
    let timer = durationInSeconds; // Durée initiale du chronomètre en secondes

    // Fonction qui met à jour le chrono et l'affiche
    function updateTimer() {
        const minutes = Math.floor(timer / 60);
        let seconds = timer % 60;

        // Ajout d'un zéro devant le nombre si les secondes sont inférieures à 10
        seconds = seconds < 10 ? '0' + seconds : seconds;

        // Affichage du chrono
        document.getElementById('chrono-button').textContent = minutes + ':' + seconds;

        // Décrémentation du chrono
        if (--timer < 0) {
            clearInterval(countdownInterval); // Arrêter le compte à rebours lorsque le temps est écoulé
            endGame();
            // alert('Time is up!'); // Afficher un message lorsque le temps est écoulé (vous pouvez modifier cela selon vos besoins)
        }
    }

    // Appel de la fonction updateTimer toutes les secondes
        updateTimer();
        countdownInterval = setInterval(updateTimer, 1000); // Mettre à jour le chrono toutes les 1000 ms (1 seconde)
    }

    function startGame() {
        if (player1Chosen && player2Chosen) {
            if (role === 'player1') {
                // Joueur 1 est l'hôte, démarrer le jeu
                startTimer(60);
                draw(); // Dessiner sur le canvas (côté hôte)
            } else if (role === 'player2') {
                // Joueur 2 est le spectateur
                setInterval(updateSpectatorCanvas, 1000);
            }
        }
    }
});

*/ 