import random
from typing import Optional, List
from card import Card


class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in Card.SUITS for rank in Card.RANKS]
        self.cards.append(Card('JOKER', 'Joker'))
        self.cards.append(Card('JOKER', 'Joker'))
        self.shuffle()
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def draw(self) -> Optional[Card]:
        return self.cards.pop() if self.cards else None
    
    def has_cards(self) -> bool:
        return len(self.cards) > 0
    
    def get_remaining_cards(self) -> List[Card]:
        return self.cards.copy()
