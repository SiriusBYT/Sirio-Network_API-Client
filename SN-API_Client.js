/* Sirio Network API*/
function SirioAPI(API_Request) {
    return new Promise(function(Success) {
        const Trinity = new WebSocket("wss://trinity.sirio-network.com");
        // const Trinity = new WebSocket("ws://localhost:1407");
        Trinity.onopen = function(e) {
            log(`[SN-API] Sending Request "${API_Request}"`)
            Trinity.send(API_Request);
        };

        Trinity.onmessage = function(event) {
            Success(event.data);
        }

        Trinity.onclose = function(event) {
            if (event.wasClean) {
                log(`[SN-API] Connection closed. Code=${event.code} Reason=${event.reason}`);
                return "Fuck"
            } else {
                log("[SN-API] Connection closed forcefully.");
                return "Fuck"
            }
        }
    });
};