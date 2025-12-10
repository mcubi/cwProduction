# HELLO, THIS IS THE MINIMAL CODE UNIF FOR CHANNELS !
# This module contains the event handling for connections => asyncConsumer bassed !

# module imports:
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import GameXO
from .utils import check_winner


class GameConsumer(AsyncWebsocketConsumer):

    # ---------------------------------------------------------
    # 1) CONNECT: el usuario entra al WebSocket
    # ---------------------------------------------------------
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_id = f"game_{self.room_id}"

        # Unirse al grupo
        await self.channel_layer.group_add(
            self.room_group_id, self.channel_name
        )

        # Aceptar conexión WebSocket
        await self.accept()

        # Obtener el juego
        game = await self.get_game()
        if not game:
            return

        # Asignar X y O automáticamente
        player_x, player_o = await self.get_players(game)
        user = self.scope["user"]

        if not player_x:
            game.player_x = user
        elif not player_o and user != player_x:
            game.player_o = user

        await self.save_game(game)

        # Enviar estado inicial
        await self.send_game_state(game)

    # ---------------------------------------------------------
    # 2) DISCONNECT
    # ---------------------------------------------------------
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_id, self.channel_name
        )

    # ---------------------------------------------------------
    # 3) RECEIVE
    # ---------------------------------------------------------
    async def receive(self, text_data):
        data = json.loads(text_data)

        if data["type"] == "move":
            await self.handle_move(data["cell"])
        elif data["type"] == "chat":
            await self.channel_layer.group_send(
                self.room_group_id,
                {
                    "type": "chat_message",
                    "message": data["message"],
                    "username": self.scope["user"].username,
                }
            )

    # ---------------------------------------------------------
    # HANDLER DEL CHAT
    # ---------------------------------------------------------
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "chat",
            "username": event["username"],
            "message": event["message"],
        }))

    # ---------------------------------------------------------
    # 4) LÓGICA DEL MOVIMIENTO DEL TRES EN RAYA
    # ---------------------------------------------------------
    async def handle_move(self, pos):
        game = await self.get_game()
        if not game:
            return

        # Solo si el juego está activo
        if game.state != "active":
            return

        board = list(game.board)
        pos = int(pos)

        # Solo si la celda está libre
        if board[pos] == "_":
            # Verificar turno del jugador
            current_user = self.scope["user"]
            player_symbol = "X" if game.player_x_id == current_user.id else "O"
            if player_symbol != game.active_player:
                return  # no es su turno

            board[pos] = game.active_player
            winner = check_winner(board)

            # Actualizar estado
            game.board = "".join(board)
            if winner == "tie":
                game.state = "tie"
            elif winner:
                game.state = "won"
                game.winner = winner
            else:
                # Alternar turno
                game.active_player = "O" if game.active_player == "X" else "X"

            await self.save_game(game)

        # Broadcast
        await self.channel_layer.group_send(
            self.room_group_id,
            {
                "type": "game_update",
                "game": await self.serialize_game(game)
            }
        )

    # ---------------------------------------------------------
    # 5) BROADCAST
    # ---------------------------------------------------------
    async def game_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "game_state",
            "game": event["game"]
        }))

    # ---------------------------------------------------------
    # 6) HELPERS BD
    # ---------------------------------------------------------
    @database_sync_to_async
    def get_game(self):
        try:
            return GameXO.objects.get(room_name=self.room_id)
        except GameXO.DoesNotExist:
            return None

    @database_sync_to_async
    def save_game(self, game):
        game.save()

    @database_sync_to_async
    def serialize_game(self, game):
        return {
            "id": game.id,
            "room_name": game.room_name,
            "board": game.board,
            "state": game.state,
            "active_player": game.active_player,
            "winner": game.winner,
            "player_x": game.player_x.username if game.player_x else None,
            "player_o": game.player_o.username if game.player_o else None,
        }

    @database_sync_to_async
    def get_players(self, game):
        return game.player_x, game.player_o

    # Enviar estado inicial
    async def send_game_state(self, game):
        await self.send(text_data=json.dumps({
            "type": "game_state",
            "game": await self.serialize_game(game),
        }))
