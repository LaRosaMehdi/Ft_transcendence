function showConfirmation() {
    document.getElementById('confirmationModal').style.display = 'block';
}

function hideConfirmation() {
    document.getElementById('confirmationModal').style.display = 'none';
}

function getTournamentNameFromUrl() {
    const urlParts = window.location.pathname.split('/');
    return urlParts[2];
}

function getGameIdFromUrl() {
    const urlParts = window.location.pathname.split('/');
    return urlParts[4];
}

function enfOfGameLoop() {
    fetch('/users/get_current_game/')
    .then(response => response.json())
    .then(data => {
        if (data.current_game === null) {
            let tournament_name = getTournamentNameFromUrl();
            window.location.href = '/tournaments/' + tournament_name + '/';
            return;
        }
    })
    .catch(error => console.error('Error:', error));
}

function drawPlayers(ctx, player1, player2) {
    ctx.fillStyle = player1.color;
    ctx.fillRect(player1.x, player1.y, player1.width, player1.height);

    ctx.fillStyle = player2.color;
    ctx.fillRect(player2.x, player2.y, player2.width, player2.height);
}

function initializeGameTournament() {
    console.log("localtournament.js call");
    const canvas = document.getElementById('pongCanvas');
    if (!canvas) {
        return;
    }
    console.log("localtournament.js call2");
    const ctx = canvas.getContext('2d');

    //new modfi JWT
    const csrfToken = localStorage.getItem('csrf_token');
    const jwtToken = localStorage.getItem('access_token');
    //manage the NULL
    if (!csrfToken || !jwtToken) {
        console.error('CSRF token or JWT token is missing');
        alert('Your session has expired. Please log in again.');
        window.location.href = '/login';  // Redirect to login page or handle appropriately
        return;
    }


    const player1 = {
        x: 50,
        y: canvas.height / 2 - 50,
        width: canvas.width / 50,
        height: canvas.height / 3,
        color: 'blue',
        speed: 5,
        keys: ['ArrowUp', 'ArrowDown']
    };

    const player2 = {
        x: canvas.width - 60,
        y: canvas.height / 2 - 50,
        width: canvas.width / 50,
        height: canvas.height / 3,
        color: 'red',
        speed: 5,
        keys: ['w', 's']
    };

    const keysPressed = {
        'ArrowUp': false,
        'ArrowDown': false,
        'w': false,
        's': false
    };

    let scorePlayer1 = 0;
    let scorePlayer2 = 0;

    let player1Chosen = false;
    let player2Chosen = false;

    function choosePlayer(player) {
        if (player === 'player1') {
            player1Chosen = true;
        } else if (player === 'player2') {
            player2Chosen = true;
        }

    }

    document.getElementById('play-btn').addEventListener('click', function() {
        canvas.style.visibility = 'visible';
        console.log("play btn call");
        startGame();
    });

    document.getElementById('player1-btn').addEventListener('click', function() {
        choosePlayer('player1');
    });

    document.getElementById('player2-btn').addEventListener('click', function() {
        choosePlayer('player2');
    });

    document.getElementById('quit_game').addEventListener('click', function() {
        canvas.style.visibility = 'visible';
        endGame(getGameIdFromUrl());
    });


    function handleKeyEvents(event) {
        if (player1.keys.includes(event.key)) {
            event.preventDefault();
            if (event.key === player1.keys[0] && player1.y > 0) {
                player1.y -= player1.speed;
            } else if (event.key === player1.keys[1] && player1.y + player1.height < canvas.height) {
                player1.y += player1.speed;
            }
        }

        if (player2.keys.includes(event.key)) {
            event.preventDefault();
            if (event.key === player2.keys[0] && player2.y > 0) {
                player2.y -= player2.speed;
            } else if (event.key === player2.keys[1] && player2.y + player2.height < canvas.height) {
                player2.y += player2.speed;
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
    const baseBallSpeed = 1;
    let currentBallSpeed = baseBallSpeed;

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
        ball.dx = 0;
        ball.dy = 0;
    }

    function resetBall() {
        ball.x = canvas.width / 2;
        ball.y = canvas.height / 2;
        ball.dx = -ball.dx;
        ball.dy = -ball.dy;
        currentBallSpeed = baseBallSpeed;
        ball.dx = Math.sign(ball.dx) * baseBallSpeed;
        ball.dy = Math.sign(ball.dy) * baseBallSpeed;
        player1.y = canvas.height / 2 - 50;
        player2.y = canvas.height / 2 - 50;
    }

    function handleCollision() {
        if (ball.y - ball.radius <= 0 || ball.y + ball.radius >= canvas.height) {
            ball.dy = -ball.dy;
        }
        if (ball.x - ball.radius <= 1) {
            scorePlayer2++;
            resetBall();
            return;
        }
        if (ball.x + ball.radius >= canvas.width - 1) {
            scorePlayer1++;
            resetBall();
            return;
        }
        if (ball.x - ball.radius <= player1.x + player1.width &&
            ball.x - ball.radius >= player1.x &&
            ball.y + ball.radius >= player1.y &&
            ball.y - ball.radius <= player1.y + player1.height) {
            ball.dx = -ball.dx;
            currentBallSpeed += accelerationRate;
            ball.x = player1.x + player1.width + ball.radius;
        }
        if (ball.x + ball.radius >= player2.x &&
            ball.x + ball.radius <= player2.x + player2.width &&
            ball.y + ball.radius >= player2.y &&
            ball.y - ball.radius <= player2.y + player2.height) {
            ball.dx = -ball.dx;
            currentBallSpeed += accelerationRate;
            ball.x = player2.x - ball.radius;
        }
    }

    function drawScores() {
        ctx.font = '24px Arial';
        ctx.fillStyle = 'white';
        ctx.fillText('Player 1: ' + scorePlayer1, 20, 30);
        ctx.fillText('Player 2: ' + scorePlayer2, canvas.width - 150, 30);

    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = 'black';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.beginPath();
        ctx.strokeStyle = 'white';
        ctx.lineWidth = 2;
        ctx.moveTo(canvas.width / 2, 0);
        ctx.lineTo(canvas.width / 2, canvas.height);
        ctx.stroke();
        drawPlayers(ctx, player1, player2);
        drawBall();
        drawScores();
        movePlayers();
        handleCollision();
        if (scorePlayer1 >= 2 || scorePlayer2 >= 2) {
            
            endGame(getGameIdFromUrl());
            return;
        }

        ball.dx += accelerationRate * Math.sign(ball.dx);
        ball.dy += accelerationRate * Math.sign(ball.dy);

        ball.x += ball.dx;
        ball.y += ball.dy;
        requestAnimationFrame(draw);
        
    }
    
    function endGame(gameId) {
        const player1Score = scorePlayer1;
        const player2Score = scorePlayer2;
        const tournament_name = getTournamentNameFromUrl();

        console.log(scorePlayer1, scorePlayer2);
        const obj = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
                'Authorization': `Bearer ${jwtToken}`
            },
            body: JSON.stringify({
                game_id: gameId,
                player1_score: player1Score,
                player2_score: player2Score
            }),
        };

        fetch(`/tournaments/${tournament_name}/play/${gameId}/end/`, obj)  // Update the URL
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Game finished successfully:', data);
            if (data.status === 'success') {
                loadPageTournament(tournament_name);
                // window.location.href = '/tournaments/' + tournament_name + '/';
            } else {
                console.error('Error ending game:', data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    
        let winner, loser;
        if (scorePlayer1 > scorePlayer2) {
            winner = "Player 1";
            loser = "Player 2";
        } else if (scorePlayer2 > scorePlayer1) {
            winner = "Player 2";
            loser = "Player 1";
        } else {
            winner = "No one (draw)";
            loser = "No one (draw)";
        }
        alert(`Time is up! ${winner} wins the game with ${Math.max(scorePlayer1, scorePlayer2)} points against ${loser} with ${Math.min(scorePlayer1, scorePlayer2)} points.`);
        resetBall();
        stopBall();
    }
    

    

    function startTimer(durationInSeconds) {
        let timer = durationInSeconds;

        function updateTimer() {
            const minutes = Math.floor(timer / 60);
            let seconds = timer % 60;

            seconds = seconds < 10 ? '0' + seconds : seconds;

            document.getElementById('chrono-button').textContent = minutes + ':' + seconds;

            if (timer-- <= 0) {
                clearInterval(countdownInterval);
                endGame();
            }
        }

        updateTimer();
        countdownInterval = setInterval(updateTimer, 1000);
    }

    

    function startGame() {
        draw();
    }

    if (document.body.classList.contains('pong-game-page')) {
        setInterval(enfOfGameLoop, 1000);
    }
}

document.addEventListener('DOMContentLoaded', initializeGame);
