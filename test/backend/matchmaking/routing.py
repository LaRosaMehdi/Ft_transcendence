# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from django.urls import path
# from matchmaking.consumers import MatchmakingConsumer

# websocket_urlpatterns = [
#     path('ws/matchmaking/', MatchmakingConsumer.as_asgi()),
# ]

# application = ProtocolTypeRouter({
#     'websocket': AuthMiddlewareStack(
#         URLRouter(
#             websocket_urlpatterns
#         )
#     ),
# })