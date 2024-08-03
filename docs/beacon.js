// Description: This script sends a beacon request to the server.
// The request contains the referrer header with the value of the current origin.
// Use the "data-addr attribute" to specify the server address.

(function (addr) {
    window.addEventListener("DOMContentLoaded", () => {
        fetch(addr, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                origin: window.location.origin,
                path: window.location.pathname,
            }),
        });
    });
})(document.currentScript.getAttribute("data-addr"));
