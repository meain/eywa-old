# For django channels
from channels.routing import route
from ai.consumers import ws_message

channel_routing = [
    route("http.request", "ai.consumers.http_consumer"),
]

channel_routing = [
    route("websocket.receive", ws_message),
]
