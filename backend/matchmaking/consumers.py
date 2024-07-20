# import json
# from channels.generic.websocket import WebsocketConsumer
# from .models import MatchmakingQueue

# class MatchmakingConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()

#     def disconnect(self, close_code):
#         pass

#     def receive(self, text_data):
#         data = json.loads(text_data)
#         action = data.get('action')

#         if action == 'requestMatchmaking':
#             self.handle_matchmaking_request()

#     def handle_matchmaking_request(self):
#         # Logique de matchmaking : recherche de matchs lorsque suffisamment de joueurs sont en attente
#         matchmaking_queue = MatchmakingQueue.objects.first()
#         if matchmaking_queue.players.count() >= 2:
#             players = list(matchmaking_queue.players.all())
#             # Assurez-vous de retirer les joueurs de la file d'attente après avoir trouvé un match
#             matchmaking_queue.players.clear()
#             # Envoyer une notification à chaque joueur avec les informations sur leur adversaire
#             for player in players:
#                 opponent = players[1] if player == players[0] else players[0]
#                 self.send(json.dumps({
#                     'action': 'matchFound',
#                     'opponentInfo': {
#                         'username': opponent.username,
#                         # Ajoutez d'autres informations sur l'adversaire si nécessaire
#                     }
                }))

