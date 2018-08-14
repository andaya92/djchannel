from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import mychannel.routing

application = ProtocolTypeRouter({
	# http->Django Views added by default
	'websocket' : AuthMiddlewareStack(URLRouter(
			mychannel.routing.websocket_urlpatterns
		)),
})