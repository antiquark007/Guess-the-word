const FASTAPI_URL = "http://127.0.0.1:8000";


// REGISTER
const registerForm = document.getElementById("register-form");

if (registerForm) {

    registerForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();

            const username =
                document.getElementById("username").value;

            const password =
                document.getElementById("password").value;

            const role =
                document.querySelector('input[name="role"]:checked').value;

            const response = await fetch(
                `${FASTAPI_URL}/api/register?username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}&role=${role}`,
                {
                    method: "POST"
                }
            );

            const data = await response.json();

            document.getElementById("message")
                .innerText = data.message || data.detail;
        }
    );
}


// LOGIN
const loginForm = document.getElementById("login-form");

if (loginForm) {

    loginForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();

            const username =
                document.getElementById("username").value;

            const password =
                document.getElementById("password").value;

            const response = await fetch(
                `${FASTAPI_URL}/api/login?username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
                {
                    method: "POST"
                }
            );

            const data = await response.json();

            if (response.ok) {

                localStorage.setItem(
                    "access_token",
                    data.access_token
                );

                localStorage.setItem(
                    "username",
                    data.username
                );

                localStorage.setItem(
                    "role",
                    data.role
                );

                window.location.href = data.role === "ADMIN"
                    ? "/admin-reports/"
                    : "/game/";

            } else {

                document.getElementById("message")
                    .innerText = data.detail;
            }
        }
    );
}