from django.db import models
from django.contrib.auth.models import User

# MODELS USED TO CREATE GAMES :: 

class GameXO(models.Model):
    STATE_CHOICES = [
        ('active', 'Active'),
        ('won', 'Won'),
        ('tie', 'Tie'),
    ]
    # room identifier 
    room_name = models.CharField(max_length=100, unique=True)
    
    # players X and O
    player_x = models.ForeignKey(
        User,
        related_name="games_as_x",
        on_delete=models.CASCADE
    )
    player_o = models.ForeignKey(
        User,
        related_name="games_as_o",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    # table state
    board = models.CharField(max_length=9, default="_________")
    
    # turn of players (first move for 'X' by default)
    active_player = models.CharField(max_length=1, default="X")
    
    # game state
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default="active")
    
    # winner
    winner = models.CharField(max_length=1, null=True, blank=True)
    
    # date (added 2nd migration)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_name