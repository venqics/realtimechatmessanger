from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path, re_path
from public_chat.consumers import PublicChatConsumer
from chat.consumers import ChatConsumer
from notification.consumers import NotificationConsumer

application = ProtocolTypeRouter({
	'websocket': AllowedHostsOriginValidator(
		AuthMiddlewareStack(
			# URLRouter([...]) # Empty for now because we don't have a consumer yet.
		URLRouter([
					path('public_chat/<room_id>/', PublicChatConsumer),
					path('chat/<room_id>/', ChatConsumer),
					path('', NotificationConsumer),
			])
        
        )
	),
})