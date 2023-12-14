import { inject } from "vue";

export function formatNumbers(i) {
    return i.toString().padStart(2, "0")
}

export function dateFormatter(d) {
    return `${formatNumbers(d.getDay())}.${formatNumbers(d.getMonth())}.${d.getFullYear()}, ${formatNumbers(d.getHours())}:${formatNumbers(d.getMinutes())} Uhr`
}

export function parseJwt(token) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(window.atob(base64, "base64").toString("ascii").split("").map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
}
