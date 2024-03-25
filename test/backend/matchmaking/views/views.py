# from django.http import JsonResponse
# from matchmaking import models
# from channels.generic.websocket import AsyncWebsocketConsumer

# class WebSocketConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass  # Ajoutez ici la logique pour gérer la déconnexion du WebSocket

# async def add_to_queue(request):
#     if request.method == 'POST':
#         user_id = request.POST.get('user_id')
#         # Logique pour ajouter l'utilisateur à la file d'attente
#         # Vous devez ajouter l'utilisateur à la file d'attente dans votre modèle MatchmakingQueue
#         # et renvoyer une réponse appropriée
#         return JsonResponse({'status': 'success'})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Invalid request method'})