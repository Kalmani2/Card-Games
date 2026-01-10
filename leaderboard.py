import json
import os
from typing import List, Dict


class Leaderboard:
    def __init__(self, filename: str = "leaderboard.json"):
        self.filename = filename
        self.scores = self._load_scores()
    
    def _load_scores(self) -> List[Dict]:
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def _save_scores(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.scores, f, indent=2)
        except IOError:
            pass
    
    def add_score(self, player_name: str, score: int, streak: int):
        entry = {
            'name': player_name,
            'score': score,
            'streak': streak
        }
        self.scores.append(entry)
        self.scores.sort(key=lambda x: x['score'], reverse=True)
        self.scores = self.scores[:50]
        self._save_scores()
    
    def get_top_scores(self, limit: int = 10) -> List[Dict]:
        return self.scores[:limit]
    
    def is_high_score(self, score: int) -> bool:
        if len(self.scores) < 10:
            return score > 0
        return score > self.scores[9]['score']
    
    def clear(self):
        self.scores = []
        self._save_scores()
