function showConfirmation() {
    document.getElementById('confirmationModal').style.display = 'block';
}

function hideConfirmation() {
    document.getElementById('confirmationModal').style.display = 'none';
}


// function enfOfGameLoop() {
//     fetch('/users/get_current_game/')
//     .then(response => response.json())
//     .then(data => {
//         if (data.current_game === null) {
//             console.log("spirit loop");
//             window.location.href = '/games/results/';
//         }
//     })
//     .catch(error => console.error('Error:', error));
// }


function drawPlayersLocal(ctx, player1, player2) {
    ctx.fillStyle = player1.color;
    ctx.fillRect(player1.x, player1.y, player1.width, player1.height);

    ctx.fillStyle = player2.color;
    ctx.fillRect(player2.x, player2.y, player2.width, player2.height);
}

function initializeGame() {
    
    const canvas = document.getElementById('pongCanvas');
    if (!canvas) {
        return;
    }
    const ctx = canvas.getContext('2d');

    //new modfi JWT
    const csrfToken = localStorage.getItem('csrf_token');
    const jwtToken = localStorage.getItem('access_token');
     const player1Name = localStorage.getItem('username');
    const player2Name = localStorage.getItem('opponent_name');
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
        speed: 10,
        keys: ['w', 's']
    };

    const player2 = {
        x: canvas.width - 60,
        y: canvas.height / 2 - 50,
        width: canvas.width / 50,
        height: canvas.height / 3,
        color: 'red',
        speed: 10,
        keys: ['ArrowUp', 'ArrowDown']
    };

    const keysPressed = {
        'ArrowUp': false,
        'ArrowDown': false,
        'w': false,
        's': false
    };

    let gamePaused = false;
    let savedBallPosition = { dx: 0, dy: 0 };
    let savedBallSpeed = 0;
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

    document.getElementById('play-btn1').addEventListener('click', function() {
        canvas.style.visibility = 'visible';
        startGameLocal();
    });


    document.getElementById('quit_game_local').addEventListener('click', function() {
        canvas.style.visibility = 'visible';
        endGameLocal();
    });


    function handleKeyEventsLocal(event) {
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

    document.addEventListener('keydown', handleKeyEventsLocal);

    function handleKeyDownLocal(event) {
        if (keysPressed.hasOwnProperty(event.key)) {
            keysPressed[event.key] = true;
        if (event.key === ' ') {
                gamePaused = !gamePaused;
                if (gamePaused) {
                    // Save current ball speed and position, then stop the ball
                    savedBallSpeed = currentBallSpeed;
                    savedBallPosition.dx = ball.dx;
                    savedBallPosition.dy = ball.dy;
                    currentBallSpeed = 0;  
                    ball.dx = 0;
                    ball.dy = 0;
                } else {
                    // Restore ball speed and position
                    currentBallSpeed = savedBallSpeed;
                    ball.dx = savedBallPosition.dx;
                    ball.dy = savedBallPosition.dy;
                }
            }
        }
    }

    function handleKeyUpLocal(event) {
        if (keysPressed.hasOwnProperty(event.key)) {
            keysPressed[event.key] = false;
        }
    }

    document.addEventListener('keydown', handleKeyDownLocal);
    document.addEventListener('keyup', handleKeyUpLocal);

    function movePlayersLocal() {
     if (!gamePaused) {
            if (keysPressed['w'] && player1.y > 0) player1.y -= player1.speed;
            if (keysPressed['s'] && player1.y + player1.height < canvas.height) player1.y += player1.speed;
            if (keysPressed['ArrowUp'] && player2.y > 0) player2.y -= player2.speed;
            if (keysPressed['ArrowDown'] && player2.y + player2.height < canvas.height) player2.y += player2.speed;
        }
    }

    const accelerationRate = 0.01;
    const baseBallSpeed = 0.1;
    let currentBallSpeed = baseBallSpeed;

    const ball = {
        x: canvas.width / 2,
        y: canvas.height / 2,
        radius: 10,
        dx: 2,
        dy: -2
    };

    function drawBallLocal() {
        ctx.beginPath();
        ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
        ctx.fillStyle = 'red';
        ctx.fill();
        ctx.closePath();
    }

    function stopBallLocal() {
        ball.dx = 0;
        ball.dy = 0;
    }

    function resetBallLocal() {
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

    function handleCollisionLocal() {
        if (ball.y - ball.radius <= 0 || ball.y + ball.radius >= canvas.height) {
            ball.dy = -ball.dy;
        }
        if (ball.x - ball.radius <= 1) {
            scorePlayer2++;
            resetBallLocal();
            return;
        }
        if (ball.x + ball.radius >= canvas.width - 1) {
            scorePlayer1++;
            resetBallLocal();
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

    function drawScoresLocal() {
        ctx.font = '24px Arial';
        ctx.fillStyle = 'white';
        ctx.fillText(player1Name + ': ' + scorePlayer1, 20, 30);
        ctx.fillText(player2Name + ': ' + scorePlayer2, canvas.width - 150, 30);

    }

    function drawLocal() {
          if (!gamePaused) {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = 'black';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.beginPath();
            ctx.strokeStyle = 'white';
            ctx.lineWidth = 2;
            ctx.moveTo(canvas.width / 2, 0);
            ctx.lineTo(canvas.width / 2, canvas.height);
            ctx.stroke();
            drawPlayersLocal(ctx, player1, player2);
            drawBallLocal();
            drawScoresLocal();
            movePlayersLocal();
            handleCollisionLocal();
            if (scorePlayer1 >= 2 || scorePlayer2 >= 2) {
                endGameLocal();
                return;
            }

            ball.dx += accelerationRate * Math.sign(ball.dx);
            ball.dy += accelerationRate * Math.sign(ball.dy);

            ball.x += ball.dx;
            ball.y += ball.dy;
        }
        requestAnimationFrame(drawLocal);
        
    }

    function endGameLocal(game) {
        const player1Score = scorePlayer1;
        const player2Score = scorePlayer2;

        const obj = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
                'Authorization': `Bearer ${jwtToken}` //new mdif JWT
            },
            body: JSON.stringify({
                player1_score: player1Score,
                player2_score: player2Score,
            }),
        };

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
            loadPageGames('results');
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
        resetBallLocal();
        stopBallLocal();
    }

    

    // function startTimer(durationInSeconds) {
    //     let timer = durationInSeconds;

    //     function updateTimer() {
    //         const minutes = Math.floor(timer / 60);
    //         let seconds = timer % 60;

    //         seconds = seconds < 10 ? '0' + seconds : seconds;

    //         document.getElementById('chrono-button').textContent = minutes + ':' + seconds;

    //         if (timer-- <= 0) {
    //             clearInterval(countdownInterval);
    //             endGame();
    //         }
    //     }

    //     updateTimer();
    //     countdownInterval = setInterval(updateTimer, 1000);
    // }

    

    function startGameLocal() {
        drawLocal();
    }

    // if (document.body.classList.contains('pong-game-page')) {
    //     setInterval(enfOfGameLoop, 1000);
    // }
}

document.addEventListener('DOMContentLoaded', initializeGame);
