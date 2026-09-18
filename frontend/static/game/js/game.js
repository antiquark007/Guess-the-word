const FASTAPI_URL = "http://127.0.0.1:8000";

let gameId = null;
let guessCount = 0;

const startButton = document.getElementById("start-game");
const submitButton = document.getElementById("submit-guess");
const guessInput = document.getElementById("guess");

function setGameControls(enabled) {

    guessInput.disabled = !enabled;
    submitButton.disabled = !enabled;
}

function stopGame(message) {

    document.getElementById("message").innerText = message;
    setGameControls(false);
    window.alert(message);
}


function getToken() {

    return localStorage.getItem(
        "access_token"
    );
}


// START GAME

startButton.addEventListener(
        "click",
        async function() {

            const token = getToken();

            if (!token) {

                document.getElementById("message")
                    .innerText =
                    "Please login first.";

                return;
            }

            const response = await fetch(
                `${FASTAPI_URL}/api/game/start`,
                {
                    method: "POST",

                    headers: {
                        "Authorization":
                            `Bearer ${token}`
                    }
                }
            );

            const data = await response.json();

            if (!response.ok) {

                document.getElementById("message")
                    .innerText = data.detail;

                return;
            }

            gameId = data.game_id;
            guessCount = 0;

            setGameControls(true);

            document.getElementById("message")
                .innerText =
                "Game started. Guess the word!";

            document.getElementById("game-board").innerHTML = "";
        }
    );


// SUBMIT GUESS

submitButton.addEventListener(
        "click",
        async function() {

            if (!gameId) {

                document.getElementById("message")
                    .innerText =
                    "Start a game first.";

                return;
            }

            const guess = guessInput.value.trim().toUpperCase();

            if (!/^[A-Z]{5}$/.test(guess)) {
                document.getElementById("message").innerText =
                    "Enter exactly 5 letters.";
                return;
            }

            const token = getToken();

            const response = await fetch(
                `${FASTAPI_URL}/api/game/${gameId}/guess?guess=${encodeURIComponent(guess)}`,
                {
                    method: "POST",

                    headers: {
                        "Authorization":
                            `Bearer ${token}`
                    }
                }
            );

            const data = await response.json();

            if (!response.ok) {

                document.getElementById("message")
                    .innerText = data.detail;

                return;
            }

            displayGuess(
                data.guess,
                data.result
            );

            document.getElementById("message")
                .innerText = data.message;

            input.value = "";

            if (
                data.status === "WON" ||
                data.status === "LOST"
            ) {
                stopGame(data.message);
            }

            guessInput.value = "";
        }
    );


function displayGuess(
    guess,
    result
) {

    const board =
        document.getElementById("game-board");

    const row =
        document.createElement("div");

    row.classList.add("game-row");

    for (
        let i = 0;
        i < guess.length;
        i++
    ) {

        const cell =
            document.createElement("span");

        cell.classList.add("cell");

        cell.classList.add(
            result[i].toLowerCase()
        );

        cell.innerText = guess[i];

        row.appendChild(cell);
    }

    board.appendChild(row);
}