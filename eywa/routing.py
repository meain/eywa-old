# For django channels
from channels.routing import route
from ai.consumers import ws_message, http_consumer

# For http requests
channel_routing = [
    route("http.request", http_consumer),
]

# For websocket requests
channel_routing = [
    route("websocket.receive", ws_message),
]
