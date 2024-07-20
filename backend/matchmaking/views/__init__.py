from matchmaking.views.matchmaking import *
from matchmaking.views.queue import *
from matchmaking.views.views import *

# from matchmaking import models
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


# # from django.shortcuts import render
# # # from .models import MatchmakingQueue
# # from django.http import JsonResponse

# # def join_matchmaking(request):
# #     if request.method == 'POST':
# #         # Ajouter le joueur à la file d'attente
# #         user = request.user  # Utilisateur actuel
# #         matchmaking_queue = MatchmakingQueue.objects.get_or_create()[0]
# #         matchmaking_queue.players.add(user)
# #         return JsonResponse({'message': 'Vous êtes maintenant en file d\'attente pour un match.'})
# #     else:
# #         return JsonResponse({'error': 'Méthode non autorisée.'}, status=405)
    

# # from django.http import JsonResponse
# # # from .models import MatchmakingQueue

# # def add_to_queue(request):
# #     if request.method == 'POST':
# #         user_id = request.POST.get('user_id')
# #         # Logique pour ajouter l'utilisateur à la file d'attente
# #         # Vous devez ajouter l'utilisateur à la file d'attente dans votre modèle MatchmakingQueue
# #         # et renvoyer une réponse appropriée
# #         return JsonResponse({'status': 'success'})
# #     else:
# #         return JsonResponse({'status': 'error', 'message': 'Invalid request method'})