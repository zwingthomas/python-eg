"""
The State is basically thinking about your code as a state machine or a 
state algorithm. Essentially like your code can be in a variety of 
states and it cannot deviate from those. Such as an author moving
from Draft to Moderation, they can then move back to Draft, or move on
to having their writing Published. After Publishing they can only move
back to Draft. It cannot go from Published to Moderation. So in state
machine there is some reasoning and rules around how it can move
between states and why it does this.

Briefly,
- An object changes its behavior based on an internal state
- At any moment, there's a finite number of states a program can be in
- State can be encapsulated in an object


Our implementation will be logically quite simple. But it takes quite
a bit of code. Imagine a game with four states that it can be in: 
Welcome screen state, Playing state, Paused state, End game state. 
So we have the option to go back and forth between these states.

"""

from __future__ import annotations
import random
from abc import ABC, abstractmethod


class Game:
    def __init__(self):
        self.state = WelcomeScreenState(self)

    def change_state(self, state):
        self.state = state


class State(ABC):
    def __init__(self, game: Game):
        self.game = game
        print(f"Currently in {self} state")

    @abstractmethod
    def on_welcome_screen(self):
        ...

    @abstractmethod
    def on_playing(self):
        ...

    @abstractmethod
    def on_break(self):
        ...

    @abstractmethod
    def on_end_game(self):
        ...


class WelcomeScreenState(State):
    def on_welcome_screen(self):
        print("Currently on welcome screen")

    def on_playing(self):
        self.game.change_state(PlayingState(self.game))

    def on_break(self):
        print("From welcome to break not allowed")

    def on_end_game(self):
        print("From welcome to endgame not allowed")


class PlayingState(State):
    def on_welcome_screen(self):
        print("From playing to welcome not allowed")

    def on_playing(self):
        print("Currently playing")

    def on_break(self):
        self.game.change_state(BreakState(self.game))

    def on_end_game(self):
        self.game.change_state(EndGameState(self.game))


class BreakState(State):
    def on_welcome_screen(self):
        print("From break to welcome not allowed")

    def on_playing(self):
        self.game.change_state(PlayingState(self.game))

    def on_break(self):
        print("Currently on break")

    def on_end_game(self):
        print("From break to end game not allowed")


class EndGameState(State):
    def on_welcome_screen(self):
        self.game.change_state(WelcomeScreenState(self.game))

    def on_playing(self):
        print("From end game to playing not allowed")

    def on_break(self):
        print("From end game to break not allowed")

    def on_end_game(self):
        print("Currently on end game")


if __name__ == "__main__":
    game = Game()

    for i in range(20):
        state = random.randrange(4)
        if state == 0:
            print("Move to welcome")
            game.state.on_welcome_screen()
        if state == 1:
            print("Move to playing")
            game.state.on_playing()
        if state == 2:
            print("Move to break")
            game.state.on_break()
        if state == 3:
            print("Move to end game")
            game.state.on_end_game()
