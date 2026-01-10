from typing import Optional, Tuple
from deck import Deck
from card import Card


class Game:
    def __init__(self):
        self.deck = Deck()
        self.current_card = None
        self.score = 0
        self.streak = 0
        self.is_over = False
        self.has_shield = False
        self.double_or_nothing_active = False
        self.pending_joker = None  # Stores joker type when drawn: 'shield' or 'double'
        self.joker_count = 0  # Track which joker (0=none drawn, 1=first, 2=second)
    
    def start(self):
        self.current_card = self.deck.draw()
        # Skip jokers as starting card
        while self.current_card and self.current_card.is_joker:
            self.deck.cards.insert(0, self.current_card)
            self.deck.shuffle()
            self.current_card = self.deck.draw()
    
    def make_guess(self, guess: str) -> Tuple[bool, Optional[Card], Optional[str]]:
        """Returns (is_correct, next_card, joker_type) where joker_type is 'shield', 'double', or None"""
        if self.is_over or not self.deck.has_cards():
            self.is_over = True
            return False, None, None
        
        next_card = self.deck.draw()
        if next_card is None:
            self.is_over = True
            return False, None, None
        
        # Check if it's a joker - don't evaluate guess yet
        if next_card.is_joker:
            self.joker_count += 1
            if self.joker_count == 1:
                # First joker = Shield
                self.has_shield = True
                self.pending_joker = 'shield'
            else:
                # Second joker = Double or Nothing
                self.double_or_nothing_active = True
                self.pending_joker = 'double'
            
            self.current_card = next_card
            return True, next_card, self.pending_joker
        
        # Regular card - evaluate guess
        is_correct = self._check_guess(guess, next_card)
        
        # Handle double or nothing
        if self.double_or_nothing_active:
            self.double_or_nothing_active = False
            if is_correct:
                self.score *= 2
                self.streak += 1
            else:
                self.score = self.score // 2
                self.is_over = True
            self.current_card = next_card
            return is_correct, next_card, None
        
        if is_correct:
            self.streak += 1
            multiplier = self._get_multiplier()
            self.score += multiplier
            self.current_card = next_card
        else:
            # Check for shield
            if self.has_shield:
                self.has_shield = False
                self.streak = 0  # Reset streak but don't end game
                self.current_card = next_card
                return False, next_card, 'shield_used'
            else:
                self.is_over = True
        
        return is_correct, next_card, None
    
    def _check_guess(self, guess: str, next_card: Card) -> bool:
        if guess == 'higher':
            return next_card.value > self.current_card.value
        elif guess == 'lower':
            return next_card.value < self.current_card.value
        elif guess == 'same':
            return next_card.value == self.current_card.value
        return False
    
    def _get_multiplier(self) -> int:
        if self.streak < 3:
            return 1
        elif self.streak < 6:
            return 2
        else:
            return 3
    
    def get_multiplier(self) -> int:
        return self._get_multiplier()
    
    def get_remaining_cards(self):
        return self.deck.get_remaining_cards()
    
    def calculate_probabilities(self) -> dict:
        """Calculate probabilities of higher/lower/same based on remaining deck"""
        if not self.current_card or self.current_card.is_joker:
            return {'higher': 0.0, 'lower': 0.0, 'same': 0.0, 'joker': 0.0}
        
        remaining = self.deck.get_remaining_cards()
        if not remaining:
            return {'higher': 0.0, 'lower': 0.0, 'same': 0.0, 'joker': 0.0}
        
        current_value = self.current_card.value
        total = len(remaining)
        
        higher_count = sum(1 for c in remaining if not c.is_joker and c.value > current_value)
        lower_count = sum(1 for c in remaining if not c.is_joker and c.value < current_value)
        same_count = sum(1 for c in remaining if not c.is_joker and c.value == current_value)
        joker_count = sum(1 for c in remaining if c.is_joker)
        
        return {
            'higher': (higher_count / total) * 100,
            'lower': (lower_count / total) * 100,
            'same': (same_count / total) * 100,
            'joker': (joker_count / total) * 100
        }
    
    def reset(self):
        self.deck = Deck()
        self.current_card = None
        self.score = 0
        self.streak = 0
        self.is_over = False
        self.has_shield = False
        self.double_or_nothing_active = False
        self.pending_joker = None
        self.joker_count = 0
