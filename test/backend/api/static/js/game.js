const canvas = document.getElementById('pongCanvas');
const ctx = canvas.getContext('2d');


const player1 = {
    x: 50,
    y: canvas.height / 2 - 50, // Position initiale au milieu de l'écran
    width: canvas.width / 50,
    height: canvas.height / 3,
    color: 'blue', // Couleur noire
    speed: 5 // Vitesse de déplacement
};

const player2 = {
    x: canvas.width - 60,
    y: canvas.height / 2 - 50,
    width: canvas.width / 50,
    height: canvas.height / 3,
    color: 'red',
    speed: 5
};

// Dessiner les plateformes des joueurs
function drawPlayers() {
    ctx.fillStyle = player1.color;
    ctx.fillRect(player1.x, player1.y, player1.width, player1.height);

    ctx.fillStyle = player2.color;
    ctx.fillRect(player2.x, player2.y, player2.width, player2.height);
}

// Définition des joueurs
let currentPlayer = null; // Le joueur actuellement sélectionné

// Fonction pour choisir le joueur
function choosePlayer(player) {
    currentPlayer = player;
    console.log('Player selected:', currentPlayer);
    startGame();
    canvas.style.visibility = 'visible';
    sendPlayerChoice(player);
}

// Gestion de la sélection du joueur
// Gérer le mouvement des plateformes des joueurs

function handleKeyEvents(event) {
    console.log('Touche pressée : ', event.key);
    // Si la touche '1' est pressée, choisir le joueur 1
    if (event.key === '1') {
        choosePlayer(player1);
    }
    // Si la touche '2' est pressée, choisir le joueur 2
    else if (event.key === '2') {
        choosePlayer(player2);
    }
    if (currentPlayer) {
        // Gérer le mouvement du joueur sélectionné
        if (event.key === 'w' && currentPlayer.y > 0) {
            currentPlayer.y -= currentPlayer.speed; // Déplacer vers le haut
        } else if (event.key === 's' && currentPlayer.y + currentPlayer.height < canvas.height) {
            currentPlayer.y += currentPlayer.speed; // Déplacer vers le bas
        }
    }
}
    
document.addEventListener('keydown', handleKeyEvents);


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
    // Réinitialiser la position de la balle au centre de la zone de jeu
    ball.x = canvas.width / 2;
    ball.y = canvas.height / 2;
    // Réinitialiser la direction de la balle (vous pouvez ajuster la direction selon votre logique de jeu)
    ball.dx = -ball.dx;
    ball.dy = -ball.dy;
    // Réinitialiser les positions des plateformes des joueurs
    player1.y = canvas.height / 2 - 50;
    player2.y = canvas.height / 2 - 50;
}

let timer; // Variable pour stocker l'identifiant du timer
let timeRemaining = 60; // Durée initiale du chronomètre en secondes (2 minutes 30 secondes)

function startGame() {
    clearInterval(timer); // Assurez-vous qu'aucun autre timer n'est actif

    // Démarrez le chronomètre uniquement si un joueur est sélectionné
    if (currentPlayer) {
        timer = setInterval(function () {
            updateTimerDisplay(); // Mettre à jour l'affichage du chronomètre
            if (--timeRemaining < 0) {
                clearInterval(timer);
                endGame(); // Arrêter le chronomètre une fois le temps écoulé
                // Insérer ici toute logique à effectuer une fois le chronomètre écoulé
            }
        }, 1000);
       
        // Cacher le bouton de démarrage du jeu
        // document.getElementById('chrono-button').style.visibility = 'hidden';
    }
}

function updateTimerDisplay() {
    let minutes = Math.floor(timeRemaining / 60);
    let seconds = timeRemaining % 60;

    // Formater les minutes et les secondes avec des zéros devant si nécessaire
    minutes = minutes < 10 ? "0" + minutes : minutes;
    seconds = seconds < 10 ? "0" + seconds : seconds;

    // Mettre à jour le texte du bouton avec le temps restant
    document.getElementById('chrono-button').textContent = minutes + ":" + seconds;
}

function startTimer(duration) {
    let timer = duration;
    setInterval(function () {
        let minutes = parseInt(timer / 60, 10);
        let seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        document.getElementById('chrono-button').textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            timer = 0;
            clearInterval(timer);
            // Insérer ici toute logique à effectuer une fois le chronomètre écoulé
        }
    }, 1000);

    // Mettre à jour l'affichage du chronomètre immédiatement après le démarrage
    updateTimerDisplay(duration);
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

function handleCollision() {
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
    }

    // Vérifier la collision avec le joueur 2
    if (ball.x + ball.radius >= player2.x &&
        ball.y >= player2.y && ball.y <= player2.y + player2.height) {
        ball.dx = -ball.dx; // Inverser la direction horizontale de la balle
    }
}

// Mettez en place un système de points
let scorePlayer1 = 0;
let scorePlayer2 = 0;

function drawScores() {
    ctx.font = '24px Arial';
    ctx.fillStyle = 'black';
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
    handleCollision();
    drawBall();
    drawScores();
    drawPlayers();
    ball.x += ball.dx;
    ball.y += ball.dy;

    if (ball.y + ball.dy > canvas.height - ball.radius || ball.y + ball.dy < ball.radius) {
        ball.dy = -ball.dy;
    }
    if (ball.x + ball.dx > canvas.width - ball.radius || ball.x + ball.dx < ball.radius) {
        ball.dx = -ball.dx;
    }
}

function update() {
    if (currentPlayer && timeRemaining)
        draw(); // Dessiner le jeu
    // setInterval(update, 10);
    // Vous pouvez également mettre d'autres logiques de mise à jour ici
}

console.log(canvas);
console.log(ctx);
console.log(player1);
console.log(player2);



window.onload = function() {
    setInterval(update, 16);
    updateTimerDisplay();

    const input = document.getElementById('chat-input');

    // input.addEventListener('focus', function() {
    //     input.setAttribute('placeholder', 'Type your message here...');
    //     input.style.color = '#fff'; // Change la couleur du texte de l'input
    //     input.style.opacity = '0.5'; // Rend le texte de l'input complètement opaque
    // });
    input.setAttribute('placeholder', 'Type your message here...');
    input.style.color = '#fff'; // Change la couleur du texte de l'input
    input.style.opacity = '0.5'

    input.addEventListener('input', function() {
        if (input.value === '') {
            input.setAttribute('placeholder', 'Type your message here...');
            input.style.color = '#fff'; // Change la couleur du texte de l'input
            input.style.opacity = '0.5'; // Rend le texte de l'input complètement opaque
        } else {
            input.removeAttribute('placeholder');
            input.style.color = 'initial'; // Rétablit la couleur par défaut du texte de l'input
            input.style.opacity = '1'; // Rend le texte de l'input complètement opaque
        }
        // if (input.value !== '') {
        //     label.style.display = 'none';
        // } else {
        //     label.style.display = 'block';
        // }
    });

    input.addEventListener('blur', function() {
        if (input.value === '') {
            input.setAttribute('placeholder', 'Type your message here...');
            // input.removeAttribute('placeholder');
            input.style.color = '#fff'; // Rend le texte de l'input transparent
            input.style.opacity = '0.5'; // Rend le texte de l'input complètement transparent
        }
        else if (input.value) {
            input.removeAttribute('placeholder');
            input.style.color = 'initial'; // Rend le texte de l'input transparent
            input.style.opacity = '0.2'; // Rend le texte de l'input complètement transparent
        }
    });


    document.addEventListener('keydown', function(event) {
        // Si une flèche est pressée et qu'un joueur est sélectionné
        if (!currentPlayer && (event.key === 'ArrowUp' || event.key === 'ArrowDown')) {
            // Empêcher le défilement de la page lorsque les touches de déplacement sont utilisées
            event.preventDefault();
        }
        else if (currentPlayer) {
            event.preventDefault();

            // Gérer le mouvement du joueur sélectionné
            if (event.key === 'ArrowUp' && currentPlayer.y > 0) {
                currentPlayer.y -= currentPlayer.speed; // Déplacer vers le haut
            } else if (event.key === 'ArrowDown' && currentPlayer.y + currentPlayer.height < canvas.height) {
                currentPlayer.y += currentPlayer.speed; // Déplacer vers le bas
            }
        }
    });
};

// Établir une connexion WebSocket
const socket = new WebSocket('ws://localhost:8080'); // Adresse de votre serveur WebSocket

function sendPlayerChoice(player) {
    socket.send(JSON.stringify({ playerChoice: player }));
}

// Gérer les entrées de déplacement du joueur local et recevoir les entrées de déplacement de l'autre joueur du serveur
document.addEventListener('keydown', function(event) {
    if (currentPlayer && currentPlayer === player1) {
        socket.send(JSON.stringify({ player: 'player1', key: event.key }));
    } else if (currentPlayer && currentPlayer === player2) {
        socket.send(JSON.stringify({ player: 'player2', key: event.key }));
    }
});

// Mettre à jour les positions des plateformes des joueurs en fonction des entrées reçues
socket.addEventListener('message', function(event) {
    const data = JSON.parse(event.data);
    const player = data.player;
    const key = data.key;

    if (player === 'player1') {
        handleMovement(player1, key);
    } else if (player === 'player2') {
        handleMovement(player2, key);
    }
});

function handleMovement(player, key) {
    if (key === 'w' && player.y > 0) {
        player.y -= player.speed;
    } else if (key === 's' && player.y + player.height < canvas.height) {
        player.y += player.speed;
    }
}