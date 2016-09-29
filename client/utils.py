import enum


class Game(enum.Enum):
    ACE = 1
    TWO = 2
    THREE = 3

print(Game.ACE < Game.TWO)
Rank = enum.Enum('Rank', 'ACE TWO THREE FOUR FIVE SIX SEVEN EIGHT NINE TEN JACK QUEEN KING')
Suit = enum.Enum('Suit', 'SPADES DIAMONDS HEARTS CLUBS JOKER')

