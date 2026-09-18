const FASTAPI_URL = "http://127.0.0.1:8000";


function getToken() {

    return localStorage.getItem(
        "access_token"
    );
}


// DAILY REPORT

document
    .getElementById("get-day-report")
    .addEventListener(
        "click",
        async function() {

            const date =
                document.getElementById(
                    "report-date"
                ).value;

            const token = getToken();

            const response = await fetch(
                `${FASTAPI_URL}/api/admin/report/day?report_date=${date}`,
                {
                    headers: {
                        "Authorization":
                            `Bearer ${token}`
                    }
                }
            );

            const data =
                await response.json();

            if (!response.ok) {

                document.getElementById(
                    "day-report"
                ).innerText = data.detail;

                return;
            }

            document.getElementById(
                "day-report"
            ).innerHTML = `

                <p>Date: ${data.date}</p>

                <p>
                    Users:
                    ${data.number_of_users}
                </p>

                <p>
                    Correct guesses:
                    ${data.number_of_correct_guesses}
                </p>
            `;
        }
    );


// USER REPORT

document
    .getElementById("get-user-report")
    .addEventListener(
        "click",
        async function() {

            const userId =
                document.getElementById(
                    "user-id"
                ).value;

            const token = getToken();

            const response = await fetch(
                `${FASTAPI_URL}/api/admin/report/user/${userId}`,
                {
                    headers: {
                        "Authorization":
                            `Bearer ${token}`
                    }
                }
            );

            const data =
                await response.json();

            if (!response.ok) {

                document.getElementById(
                    "user-report"
                ).innerText = data.detail;

                return;
            }

            let html = "";

            data.forEach(
                function(row) {

                    html += `
                        <p>
                            Date: ${row.date}
                            |
                            Words tried: ${row.words_tried}
                            |
                            Correct guesses:
                            ${row.correct_guesses}
                        </p>
                    `;
                }
            );

            document.getElementById(
                "user-report"
            ).innerHTML = html;
        }
    );