import enum


class Game(enum.Enum):
    THREE = 1
    FOUR = 2
    FIVE = 3
    SIX = 4
    SEVEN = 5
    EIGHT = 6
    NINE = 7
    TEN = 8
    JACK = 9
    QUEEN = 10
    KING = 11
    ACE = 12
    TWO = 13


print(Game.ACE.value < Game.TWO.value)
Rank = enum.Enum('Rank', 'THREE FOUR FIVE SIX SEVEN EIGHT NINE TEN JACK QUEEN KING ACE TWO')
Suit = enum.Enum('Suit', 'SPADES DIAMONDS HEARTS CLUBS JOKER')

