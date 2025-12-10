# HELLO, THIS IS THE MINIMAL CODE UNIF FOR CHANNELS !
# This module contains the event handling for connections => asyncConsumer bassed !

# module imports:
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import GameXO
from .utils import check_winner


class GameConsumer(AsyncWebsocketConsumer):

    # CONNECTION FUNCTION ::
   
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_name"] # Get room name from URL
        self.room_group_id = f"game_{self.room_id}" # Define group name based on room name

        # Group adding
        await self.channel_layer.group_add(
            self.room_group_id, self.channel_name
        )

        # WS acceptance
        await self.accept()

        # Getter for game
        game = await self.get_game()
        if not game:
            return

        # Player assignment
        player_x, player_o = await self.get_players(game)
        user = self.scope["user"]

        if not player_x:
            game.player_x = user
        elif not player_o and user != player_x:
            game.player_o = user

        await self.save_game(game)

        # Initial state sending
        await self.send_game_state(game)

    # DISCONNECTION FUNCTION ::
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_id, self.channel_name
        )

    # RECEIVE MESSAGE FUNCTION ::
    
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

    # CHAT HANDLER ::
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "chat",
            "username": event["username"],
            "message": event["message"],
        }))


    # MOVEMENT HANDLER ::
    
    async def handle_move(self, pos):
        game = await self.get_game()
        if not game:
            return

    
        if game.state != "active":
            return

        board = list(game.board)
        pos = int(pos)

        # case cell open
        if board[pos] == "_":
            
            current_user = self.scope["user"]
            player_symbol = "X" if game.player_x_id == current_user.id else "O"
            if player_symbol != game.active_player:
                return  

            board[pos] = game.active_player
            winner = check_winner(board)

            game.board = "".join(board)
            if winner == "tie":
                game.state = "tie"
            elif winner:
                game.state = "won"
                game.winner = winner
            else:
                
                game.active_player = "O" if game.active_player == "X" else "X"

            await self.save_game(game)

        # Channel layer group broadcast
        await self.channel_layer.group_send(
            self.room_group_id,
            {
                "type": "game_update",
                "game": await self.serialize_game(game)
            }
        )


    # UPDATE HANDLER FOR BRWSR ::
    
    async def game_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "game_state",
            "game": event["game"]
        }))

    # DB SYNC HELPERS ::
    
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

    # Function to send the state
    async def send_game_state(self, game):
        await self.send(text_data=json.dumps({
            "type": "game_state",
            "game": await self.serialize_game(game),
        }))
