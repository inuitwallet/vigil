$(function() {
    const webSocketBridge = new channels.WebSocketBridge();
    webSocketBridge.connect('/alert_list/');

    webSocketBridge.socket.addEventListener('open', function() {
        webSocketBridge.listen(function(data) {
            if (data["message_type"] === "update_alert") {
                var row = $('#' + data["alert_id"]);
                row.focusout();
                row.remove();
                $(data['html']).prependTo(".active-alerts > tbody");
                row.focusin();
            }
            if (data["message_type"] === 'new_alert') {
                $(data['html']).prependTo(".active-alerts > tbody");
                var row = $('#' + data["alert_id"]);
                row.focusout();
                row.focusin();
            }
        });
    });
});
