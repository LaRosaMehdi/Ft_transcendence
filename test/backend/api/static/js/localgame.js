document.addEventListener('DOMContentLoaded', function() {
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
    }
    
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

    function resetBall() {
        ball.x = canvas.width / 2;
        ball.y = canvas.height / 2;
        ball.dx = -ball.dx; // Changement de direction de la balle après chaque point marqué
        ball.dy = -ball.dy;
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
            ball.y >= player1.y && ball.y <= player1.y + player1.height) {
            ball.dx = -ball.dx; // Inverser la direction horizontale de la balle
        }
    
        // Vérifier la collision avec le joueur 2
        if (ball.x + ball.radius >= player2.x &&
            ball.y >= player2.y && ball.y <= player2.y + player2.height) {
            ball.dx = -ball.dx; // Inverser la direction horizontale de la balle
        }
    }
    
    function drawScores() {
        // Dessiner les scores ici
        ctx.font = '3% Arial';
        ctx.fillStyle = 'white';
        ctx.fillText('Player 1: ' + scorePlayer1, 20, 30);
        ctx.fillText('Player 2: ' + scorePlayer2, canvas.width - 150, 30);
    }
    
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawPlayers();
        drawBall();
        drawScores();
        movePlayers();
        handleCollision();
        ball.x += ball.dx;
        ball.y += ball.dy;
        requestAnimationFrame(draw);
    }
    
    function startGame() {
        draw();
    }
});

