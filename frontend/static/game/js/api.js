const BACKENDS = [
    "http://127.0.0.1:8081",
    "http://127.0.0.1:8000"
];

let activeBackend = BACKENDS[1];

async function detectBackend() {
    try {
        const response = await fetch(`${BACKENDS[0]}/`, {
            signal: AbortSignal.timeout(800)
        });

        if (response.ok) {
            activeBackend = BACKENDS[0];
        }
    } catch (error) {
        activeBackend = BACKENDS[1];
    }
}

const backendReady = detectBackend();

function getBackendUrl() {
    return activeBackend;
}

async function apiFetch(path, options) {
    await backendReady;

    const requestUrl = new URL(path, activeBackend);

    try {
        return await fetch(requestUrl, options);
    } catch (error) {
        const fallback = activeBackend === BACKENDS[0] ? BACKENDS[1] : BACKENDS[0];
        activeBackend = fallback;
        return fetch(`${activeBackend}${requestUrl.pathname}${requestUrl.search}`, options);
    }
}
