let accessToken = typeof window !== 'undefined' && (window.localStorage.getItem("data") && window.localStorage.getItem("data") !== 'null') ? JSON.parse(window.localStorage.getItem("data")).token : "";

let baseUrl = "https://intent-alien-crisp.ngrok-free.app"

let adminUrl = `${baseUrl}/admin`
let authUrl = `${baseUrl}/auth`
let appUrl = `${baseUrl}/api`

let headers = {
    Authorization: `Bearer ${accessToken}`,
    // "token": `Bearer ${accessToken}`,
    // "Access-Control-Allow-Credentials": true,
    // "Access-Control-Allow-Origin": '*',
}

let config = {
    headers,
    params: null,
}

export { adminUrl, authUrl, appUrl, config };