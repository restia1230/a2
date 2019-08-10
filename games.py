from __future__ import annotations
import random
from typing import Dict, Union, Optional
from players import Player
from trees import QuadTree, TwoDTree
    
class Game:

    def handle_collision(self, player1: str, player2: str) -> None:
        """ Perform some action when <player1> and <player2> collide """
        raise NotImplementedError

    def check_for_winner(self) -> Optional[str]:
        """ Return the name of the player or group of players that have
        won the game, or None if no player has won yet """
        raise NotImplementedError

class Tag(Game):
    _players: Dict[str, Player]
    field: Union[QuadTree, TwoDTree]
    _it: str
    _duration: int

    def __init__(self, n_players: int,
                       field_type: Union[QuadTree, TwoDTree],
                       duration: int,
                       max_speed: int,
                       max_vision: int) -> None:
        self.n_players = n_players
        self.field = field_type
        self._duration = duration
        self.max_speed = max_speed
        self.max_vision = max_vision
        self._players = {}
        self._it = ""

    def handle_collision(self, player1: str, player2: str) -> None:
        """ Perform some action when <player1> and <player2> collide """
        pass

    def check_for_winner(self) -> Optional[str]:
        """ Return the name of the player or group of players that have
        won the game, or None if no player has won yet
        # >>> len(t._players) == 1
        # True
        # >>> c = Player(None, None, None, None, None, None)
        # >>> t2 = Tag(3, None, 60, 1, 10)
        # >>> t2._players["player"] = p
        # >>> t2._players["eric"] = e
        # >>> t2._players["c"] = c
        # >>> len(t2._players) == 3
        # True
        # >>> t._it = "player"
        # >>> t.check_for_winner()
        # 'eric'
        # >>> len(t2._players) == 1
        # True
        >>> p = Player(None, None, None, None, None, None)
        >>> e = Player(None, None, None, None, None, None)
        >>> t = Tag(2, None, 60, 1, 10)
        >>> t._players["player"] = p
        >>> t._players["eric"] = e
        >>> len(t._players) == 2
        True
        >>> t._it = "player"
        >>> t.check_for_winner()
        'eric'
        """
        if len(self._players) > 2:
            for player in self._players:
                if self._players[player]._points >= 1 and self._it != player:
                    del self._players[player]
                    # self.field.remove(player)
            winners = [*self._players]
            return winners

        elif len(self._players) == 2:
            if self._it in self._players:
                del self._players[self._it]
                # self.field.remove(player)
            winner = [*self._players]
            return winner[0]
        else:
            winner = [*self._players]
            return winner[0]


class ZombieTag(Game):
    _humans: Dict[str, Player]
    _zombies: Dict[str, Player]
    field: Union[QuadTree, TwoDTree]
    _duration: int

    def __init__(self, n_players: int,
                       field_type: Union[QuadTree, TwoDTree],
                       duration: int,
                       max_speed: int,
                       max_vision: int) -> None:
        self.n_players = n_players
        self.field = field_type
        self._duration = duration
        self.max_speed = max_speed
        self.max_vision = max_vision
        self._humans = {}
        self._zombies = {}
        for human in self._humans:
            self._humans[human]._vision = random.randint(0, max_vision)
            self._humans[human]._speed = random.randint(0, max_speed)
        for zombie in self._zombies:
            self._zombies[zombie]._vision = self.max_vision
            self._zombies[zombie]._speed = 1

    def handle_collision(self, player1: str, player2: str) -> None:
        """ Perform some action when <player1> and <player2> collide """
        raise NotImplementedError

    def check_for_winner(self) -> Optional[str]:
        """ Return the name of the player or group of players that have
        won the game, or None if no player has won yet
        >>> p = Player(None, None, None, None, None, None)
        >>> e = Player(None, None, None, None, None, None)
        >>> c = Player(None, None, None, None, None, None)
        >>> z = ZombieTag(3, None, 60, 1, 10)
        >>> z._zombies['p'] = p
        >>> z._zombies['e'] = e
        >>> z._zombies['c'] = c
        >>> z.check_for_winner()
        ['p', 'e', 'c']
        >>> z2 = ZombieTag(3, None, 60, 1, 10)
        >>> z2._humans['p'] = p
        >>> z2._humans['e'] = e
        >>> z2._zombies['c'] = c
        >>> z2.check_for_winner()
        ['p', 'e']
        """
        if self._humans == {}:
            return [*self._zombies]
        elif len(self._humans) >= 2:
            return [*self._humans]
        else:
            winner = [*self._humans]
            return winner[0]


class EliminationTag(Game):
    _players: Dict[str, Player]
    field: Union[QuadTree, TwoDTree]

    def __init__(self, n_players: int,
                       field_type: Union[QuadTree, TwoDTree],
                       max_speed: int,
                       max_vision: int) -> None:
        self.n_players = n_players
        self.field = field_type
        self.max_speed = max_speed
        self.max_vision = max_vision
        self._players = {}

    def handle_collision(self, player1: str, player2: str) -> None:
        """ Perform some action when <player1> and <player2> collide """
        raise NotImplementedError

    def check_for_winner(self) -> Optional[str]:
        """ Return the name of the player or group of players that have
        won the game, or None if no player has won yet
        >>> p = Player(None, None, None, None, None, None)
        >>> e = Player(None, None, None, None, None, None)
        >>> c = Player(None, None, None, None, None, None)
        >>> elim = EliminationTag(3, None, 1, 10)
        >>> elim._players['p'] = p
        >>> elim._players['e'] = e
        >>> elim._players['c'] = c
        >>> elim._players['p']._points = 3
        >>> elim._players['e']._points = 2
        >>> elim._players['c']._points = 1
        >>> elim.check_for_winner()
        'p'
        """
        winner = []
        points = 0
        for player in self._players:
            if self._players[player]._points >= points:
                winner.append(player)
                points = self._players[player]._points
        if len(winner) > 1:
            return None
        else:
            return winner[0]

if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={'extra-imports': ['random', 'typing', 'players', 'trees']})

