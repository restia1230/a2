from __future__ import annotations
from typing import Optional, List, Tuple, Dict


class OutOfBoundsError(Exception):
    pass


class Tree:
    def __contains__(self, name: str) -> bool:
        """ Return True if a player named <name> is stored in this tree.

        Runtime: O(n)
        """
        raise NotImplementedError

    def contains_point(self, point: Tuple[int, int]) -> bool:
        """ Return True if a player at location <point> is stored in this tree.

        Runtime: O(log(n))
        """
        raise NotImplementedError

    def insert(self, name: str, point: Tuple[int, int]) -> None:
        """Insert a player named <name> into this tree at point <point>.

        Raise an OutOfBoundsError if <point> is out of bounds.

        Raise an OutOfBoundsError if moving the player would place the player at exactly the
        same coordinates of another player in the Tree (before moving the player).

        Runtime: O(log(n))
        """
        raise NotImplementedError

    def remove(self, name: str) -> None:
        """ Remove information about a player named <name> from this tree.

        Runtime: O(n)
        """
        raise NotImplementedError

    def remove_point(self, point: Tuple[int, int]) -> None:
        """ Remove information about a player at point <point> from this tree.

        Runtime: O(log(n))
        """
        raise NotImplementedError

    def move(self, name: str, direction: str, steps: int) -> Optional[
        Tuple[int, int]]:
        """ Return the new location of the player named <name> after moving it
        in the given <direction> by <steps> steps.

        Raise an OutOfBoundsError if this would move the player named
        <name> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player at exactly the
        same coordinates of another player in the Tree (before moving the player).

        Runtime: O(n)

        === precondition ===
        direction in ['N', 'S', 'E', 'W']
        """
        raise NotImplementedError

    def move_point(self, point: Tuple[int, int], direction: str, steps: int) -> \
            Optional[Tuple[int, int]]:
        """ Return the new location of the player at point <point> after moving it
        in the given <direction> by <steps> steps.

        Raise an OutOfBoundsError if this would move the player at point
        <point> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player at exactly the
        same coordinates of another player in the Tree (before moving the player).

        Moving a point may require the tree to be reorganized. This method should do
        the minimum amount of tree reorganization possible to move the given point properly.

        Runtime: O(log(n))

        === precondition ===
        direction in ['N', 'S', 'E', 'W']

        """
        raise NotImplementedError

    def names_in_range(self, point: Tuple[int, int], direction: str,
                       distance: int) -> List[str]:
        """ Return a list of names of players whose location is in the <direction>
        relative to <point> and whose location is within <distance> along both the x and y axis.

        For example: names_in_range((100, 100), 'SE', 10) should return the names of all
        the players south east of (100, 100) and within 10 steps in either direction.
        In other words, find all players whose location is in the box with corners at:
        (100, 100) (110, 100) (100, 110) (110, 110)

        Runtime: faster than O(n) when distance is small

        === precondition ===
        direction in ['NE', 'SE', 'NE', 'SW']
        """
        raise NotImplementedError

    def size(self) -> int:
        """ Return the number of nodes in <self>

        Runtime: O(n)
        """
        raise NotImplementedError

    def height(self) -> int:
        """ Return the height of <self>

        Height is measured as the number of nodes in the path from the root of this
        tree to the node at the greatest depth in this tree.

        Runtime: O(n)
        """
        raise NotImplementedError

    def depth(self, tree: Tree) -> Optional[int]:
        """ Return the depth of the subtree <tree> relative to <self>. Return None
        if <tree> is not a descendant of <self>

        Runtime: O(log(n))
        """

    def is_leaf(self) -> bool:
        """ Return True if <self> has no children

        Runtime: O(1)
        """
        raise NotImplementedError

    def is_empty(self) -> bool:
        """ Return True if <self> does not store any information about the location
        of any players.

        Runtime: O(1)
        """
        raise NotImplementedError


def directions(centre: Tuple[int, int], point: Tuple[int, int]) -> int:
    if point[0] > centre[0] and point[1] > centre[1]:
        return 4
    elif point[0] > centre[0] and point[1] < centre[1]:
        return 1
    elif point[0] < centre[0] and point[1] > centre[1]:
        return 3
    else:
        return 2


class QuadTree(Tree):
    _centre: Tuple[int, int]
    _name: Optional[str]
    _point: Optional[Tuple[int, int]]
    _ne: Optional[QuadTree]
    _nw: Optional[QuadTree]
    _se: Optional[QuadTree]
    _sw: Optional[QuadTree]

    def __init__(self, centre: Tuple[int, int]) -> None:
        """Initialize a new QuadTree instance

        Runtime: O(1)
        """
        self._centre = centre
        self._se = []
        self._ne = []
        self._nw = []
        self._sw = []
        self._name = ""
        self._point = ()

    def __contains__(self, name: str) -> bool:
        """ Return True if a player named <name> is stored in this tree.

        Runtime: O(n)
        """
        if self.is_empty():
            return False
        elif self._name == name:
            return True
        else:
            if self._ne.__contains__(name) or self._nw.__contains__(name) or \
                    self._se.__contains__(name) or self._sw.__contains__(name):
                return True
        return False

    def contains_point(self, point: Tuple[int, int]) -> bool:
        """ Return True if a player at location <point> is stored in this tree.

        Runtime: O(log(n))
        """
        if self.is_empty():
            return False
        elif self._point == point:
            return True
        elif point[0] > self._point[0] and point[1] > self._point[1]:
            return self._se.contains_point()
        elif point[0] > self._point[0] and point[1] < self._point[1]:
            return self._ne.contains_point()
        elif point[0] < self._point[0] and point[1] > self._point[1]:
            return self._sw.contains_point()
        elif point[0] < self._point[0] and point[1] < self._point[1]:
            return self._nw.contains_point()
        return False

    def insert(self, name: str, point: Tuple[int, int]) -> None:
        """Insert a player named <name> into this tree at point <point>.

        Raise an OutOfBoundsError if <point> is out of bounds.

        Raise an OutOfBoundsError if moving the player would place the player at exactly the
        same coordinates of another player in the Tree (before moving the player).

        Runtime: O(log(n))
        """

        if self.contains_point(point):
            raise OutOfBoundsError
        step = int(self._centre[0] / 2)
        if directions(self._centre, point) == 4:
            if self.is_empty() or self._se == []:
                newquad = QuadTree(
                    (self._centre[0] + step, self._centre[1] + step))
                self._se = newquad
                newquad._name = name
            else:
                self._se.insert(name, point)
        elif directions(self._centre, point) == 1:
            if self.is_empty() or self._ne == []:
                newquad = QuadTree(
                    (self._centre[0] + step, self._centre[1] - step))
                self._ne = newquad
                newquad._name = name
            else:
                self._ne.insert(name, point)
        elif directions(self._centre, point) == 2:
            if self.is_empty() or self._nw == []:
                newquad = QuadTree(
                    (self._centre[0] - step, self._centre[1] - step))
                self._nw = newquad
                newquad._name = name
            else:
                self._nw.insert(name, point)
        elif directions(self._centre, point) == 3:
            if self.is_empty() or self._sw == []:
                newquad = QuadTree(
                    (self._centre[0] - step, self._centre[1] + step))
                self._sw = newquad
                newquad._name = name
            else:
                self._sw.insert(name, point)

    def remove(self, name: str) -> None:
        """ Remove information about a player named <name> from this tree.

        Runtime: O(n)
        """
        raise NotImplementedError

    def remove_point(self, point: Tuple[int, int]) -> None:
        """ Remove information about a player at point <point> from this tree.

        Runtime: O(log(n))
        """
        raise NotImplementedError

    def move(self, name: str, direction: str, steps: int) -> Optional[
        Tuple[int, int]]:
        """ Return the new location of the player named <name> after moving it
        in the given <direction> by <steps> steps.

        Raise an OutOfBoundsError if this would move the player named
        <name> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player at exactly the
        same coordinates of another player in the Tree (before moving the player).

        Runtime: O(n)

        === precondition ===
        direction in ['N', 'S', 'E', 'W']
        """
        raise NotImplementedError

    def move_point(self, point: Tuple[int, int], direction: str, steps: int) -> \
            Optional[Tuple[int, int]]:
        """ Return the new location of the player at point <point> after moving it
        in the given <direction> by <steps> steps.

        Raise an OutOfBoundsError if this would move the player at point
        <point> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player at exactly the
        same coordinates of another player in the Tree (before moving the player).

        Moving a point may require the tree to be reorganized. This method should do
        the minimum amount of tree reorganization possible to move the given point properly.

        Runtime: O(log(n))

        === precondition ===
        direction in ['N', 'S', 'E', 'W']

        """
        raise NotImplementedError

    def names_in_range(self, point: Tuple[int, int], direction: str,
                       distance: int) -> List[str]:
        """ Return a list of names of players whose location is in the <direction>
        relative to <point> and whose location is within <distance> along both the x and y axis.

        For example: names_in_range((100, 100), 'SE', 10) should return the names of all
        the players south east of (100, 100) and within 10 steps in either direction.
        In other words, find all players whose location is in the box with corners at:
        (100, 100) (110, 100) (100, 110) (110, 110)

        Runtime: faster than O(n) when distance is small

        === precondition ===
        direction in ['NE', 'SE', 'NE', 'SW']
        """
        raise NotImplementedError

    def size(self) -> int:
        """ Return the number of nodes in <self>

        Runtime: O(n)
        """
        raise NotImplementedError

    def height(self) -> int:
        """ Return the height of <self>

        Height is measured as the number of nodes in the path from the root of this
        tree to the node at the greatest depth in this tree.

        Runtime: O(n)
        """
        raise NotImplementedError

    def depth(self, tree: Tree) -> Optional[int]:
        """ Return the depth of the subtree <tree> relative to <self>. Return None
        if <tree> is not a descendant of <self>

        Runtime: O(log(n))
        """

    def is_leaf(self) -> bool:
        """ Return True if <self> has no children

        Runtime: O(1)
        """
        raise NotImplementedError

    def is_empty(self) -> bool:
        """ Return True if <self> does not store any information about the location
        of any players.

        Runtime: O(1)
        """
        raise NotImplementedError


class TwoDTree(Tree):
    _name: Optional[str]
    _point: Optional[Tuple[int, int]]
    _nw: Tuple[int, int]
    _se: Tuple[int, int]
    _lt: Optional[TwoDTree]
    _gt: Optional[TwoDTree]
    _split_type: str

    def __init__(self, nw: Tuple[int, int], se: Tuple[int, int]) -> None:
        """Initialize a new Tree instance

        Runtime: O(1)
        """
        pass

    def balance(self) -> None:
        """ Balance <self> so that there is at most a difference of 1 between the
        size of the _lt subtree and the size of the _gt subtree for all trees in
        <self>.
        """
        pass


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={'extra-imports': ['typing']})
