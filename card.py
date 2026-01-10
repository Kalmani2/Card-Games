class Card:
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    SUIT_SYMBOLS = {
        'Hearts': '♥',
        'Diamonds': '♦',
        'Clubs': '♣',
        'Spades': '♠',
        'Joker': '🃏'
    }
    SUIT_COLORS = {
        'Hearts': '#E74C3C',
        'Diamonds': '#E74C3C',
        'Clubs': '#2C3E50',
        'Spades': '#2C3E50',
        'Joker': '#9C27B0'
    }
    
    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit
        self.value = self._calculate_value()
        self.is_joker = (rank == 'JOKER')
    
    def _calculate_value(self) -> int:
        if self.rank == 'JOKER':
            return 15
        elif self.rank == 'A':
            return 14
        elif self.rank == 'K':
            return 13
        elif self.rank == 'Q':
            return 12
        elif self.rank == 'J':
            return 11
        else:
            return int(self.rank)
    
    def get_symbol(self) -> str:
        if self.is_joker:
            return self.SUIT_SYMBOLS['Joker']
        return self.SUIT_SYMBOLS[self.suit]
    
    def get_color(self) -> str:
        if self.is_joker:
            return self.SUIT_COLORS['Joker']
        return self.SUIT_COLORS[self.suit]
    
    def __str__(self) -> str:
        return f"{self.rank} of {self.suit}"
    
    def __repr__(self) -> str:
        return f"{self.rank}{self.get_symbol()}"
