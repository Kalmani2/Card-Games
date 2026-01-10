import tkinter as tk
from tkinter import messagebox, simpledialog
from typing import Optional
from game import Game
from leaderboard import Leaderboard


class RemainingCardsWindow:
    def __init__(self, parent, cards):
        self.window = tk.Toplevel(parent)
        self.window.title("Remaining Cards")
        self.window.geometry("500x600")
        self.window.configure(bg='#1a1a2e')
        self.window.resizable(False, False)
        
        title = tk.Label(self.window, text=f"Remaining Cards ({len(cards)})", font=('Arial', 20, 'bold'), fg='#00d4ff', bg='#1a1a2e')
        title.pack(pady=20)
        
        canvas_frame = tk.Frame(self.window, bg='#1a1a2e')
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        canvas = tk.Canvas(canvas_frame, bg='#16213e', highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#16213e')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        sorted_cards = sorted(cards, key=lambda c: (c.value, c.suit))
        
        row, col = 0, 0
        for card in sorted_cards:
            card_frame = tk.Frame(scrollable_frame, bg='#ffffff', width=60, height=80, relief=tk.RAISED, bd=2)
            card_frame.grid(row=row, column=col, padx=5, pady=5)
            card_frame.pack_propagate(False)
            
            rank_label = tk.Label(card_frame, text=card.rank, font=('Arial', 14, 'bold'), fg=card.get_color(), bg='#ffffff')
            rank_label.pack(expand=True)
            
            suit_label = tk.Label(card_frame, text=card.get_symbol(), font=('Arial', 12), fg=card.get_color(), bg='#ffffff')
            suit_label.pack(expand=True)
            
            col += 1
            if col >= 6:
                col = 0
                row += 1
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        close_btn = tk.Button(self.window, text="Close", command=self.window.destroy, font=('Arial', 12, 'bold'), bg='#607D8B', fg='white', width=15, height=2)
        close_btn.pack(pady=(0, 20))


class LeaderboardWindow:
    def __init__(self, parent, leaderboard):
        self.window = tk.Toplevel(parent)
        self.window.title("Leaderboard")
        self.window.geometry("600x500")
        self.window.configure(bg='#1a1a2e')
        self.window.resizable(False, False)
        
        title = tk.Label(self.window, text="TOP 10 SCORES", font=('Arial', 24, 'bold'), fg='#ffd700', bg='#1a1a2e')
        title.pack(pady=20)
        
        scores_frame = tk.Frame(self.window, bg='#16213e', relief=tk.RAISED, bd=2)
        scores_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        header_frame = tk.Frame(scores_frame, bg='#16213e')
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(header_frame, text="Rank", font=('Arial', 12, 'bold'), fg='#00d4ff', bg='#16213e', width=8).grid(row=0, column=0)
        tk.Label(header_frame, text="Name", font=('Arial', 12, 'bold'), fg='#00d4ff', bg='#16213e', width=25).grid(row=0, column=1)
        tk.Label(header_frame, text="Score", font=('Arial', 12, 'bold'), fg='#00d4ff', bg='#16213e', width=12).grid(row=0, column=2)
        tk.Label(header_frame, text="Streak", font=('Arial', 12, 'bold'), fg='#00d4ff', bg='#16213e', width=12).grid(row=0, column=3)
        
        canvas = tk.Canvas(scores_frame, bg='#16213e', highlightthickness=0)
        scrollbar = tk.Scrollbar(scores_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#16213e')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        top_scores = leaderboard.get_top_scores(10)
        
        if not top_scores:
            no_scores = tk.Label(scrollable_frame, text="No scores yet. Be the first!", font=('Arial', 14), fg='#a0a0a0', bg='#16213e')
            no_scores.pack(pady=50)
        else:
            for idx, entry in enumerate(top_scores, 1):
                row_bg = '#1a1a2e' if idx % 2 == 0 else '#16213e'
                rank_color = '#ffd700' if idx == 1 else '#c0c0c0' if idx == 2 else '#cd7f32' if idx == 3 else '#a0a0a0'
                
                entry_frame = tk.Frame(scrollable_frame, bg=row_bg)
                entry_frame.pack(fill=tk.X, pady=2)
                
                tk.Label(entry_frame, text=f"#{idx}", font=('Arial', 11, 'bold'), fg=rank_color, bg=row_bg, width=6).grid(row=0, column=0)
                tk.Label(entry_frame, text=entry['name'], font=('Arial', 11), fg='#ffffff', bg=row_bg, width=25, anchor='w').grid(row=0, column=1, padx=5)
                tk.Label(entry_frame, text=str(entry['score']), font=('Arial', 11, 'bold'), fg='#00ff88', bg=row_bg, width=12).grid(row=0, column=2)
                tk.Label(entry_frame, text=str(entry['streak']), font=('Arial', 11), fg='#ff6b9d', bg=row_bg, width=12).grid(row=0, column=3)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")
        
        close_btn = tk.Button(self.window, text="Close", command=self.window.destroy, font=('Arial', 12, 'bold'), bg='#607D8B', fg='white', width=15, height=2)
        close_btn.pack(pady=(0, 20))


class ProbabilityPanel:
    def __init__(self, parent, game):
        self.parent = parent
        self.game = game
        self.window = None
        self.is_open = False
    
    def toggle(self):
        if self.is_open:
            self.close()
        else:
            self.open()
    
    def open(self):
        if self.window:
            return
        
        self.window = tk.Toplevel(self.parent)
        self.window.title("Odds Calculator")
        self.window.geometry("280x350")
        self.window.configure(bg='#1a1a2e')
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        
        # Position to the right of main window
        x = self.parent.winfo_x() + self.parent.winfo_width() + 10
        y = self.parent.winfo_y()
        self.window.geometry(f"+{x}+{y}")
        
        title = tk.Label(self.window, text="ODDS", font=('Arial', 20, 'bold'), fg='#00d4ff', bg='#1a1a2e')
        title.pack(pady=15)
        
        self.prob_frame = tk.Frame(self.window, bg='#16213e', relief=tk.RAISED, bd=2)
        self.prob_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Higher probability
        self.higher_frame = tk.Frame(self.prob_frame, bg='#16213e')
        self.higher_frame.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(self.higher_frame, text="▲ HIGHER", font=('Arial', 12, 'bold'), fg='#4CAF50', bg='#16213e', width=12, anchor='w').pack(side=tk.LEFT)
        self.higher_label = tk.Label(self.higher_frame, text="0.0%", font=('Arial', 14, 'bold'), fg='#ffffff', bg='#16213e')
        self.higher_label.pack(side=tk.RIGHT)
        self.higher_bar = tk.Canvas(self.prob_frame, height=20, bg='#0d0d1a', highlightthickness=0)
        self.higher_bar.pack(fill=tk.X, padx=10)
        
        # Same probability
        self.same_frame = tk.Frame(self.prob_frame, bg='#16213e')
        self.same_frame.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(self.same_frame, text="= SAME", font=('Arial', 12, 'bold'), fg='#2196F3', bg='#16213e', width=12, anchor='w').pack(side=tk.LEFT)
        self.same_label = tk.Label(self.same_frame, text="0.0%", font=('Arial', 14, 'bold'), fg='#ffffff', bg='#16213e')
        self.same_label.pack(side=tk.RIGHT)
        self.same_bar = tk.Canvas(self.prob_frame, height=20, bg='#0d0d1a', highlightthickness=0)
        self.same_bar.pack(fill=tk.X, padx=10)
        
        # Lower probability
        self.lower_frame = tk.Frame(self.prob_frame, bg='#16213e')
        self.lower_frame.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(self.lower_frame, text="▼ LOWER", font=('Arial', 12, 'bold'), fg='#f44336', bg='#16213e', width=12, anchor='w').pack(side=tk.LEFT)
        self.lower_label = tk.Label(self.lower_frame, text="0.0%", font=('Arial', 14, 'bold'), fg='#ffffff', bg='#16213e')
        self.lower_label.pack(side=tk.RIGHT)
        self.lower_bar = tk.Canvas(self.prob_frame, height=20, bg='#0d0d1a', highlightthickness=0)
        self.lower_bar.pack(fill=tk.X, padx=10)
        
        # Joker probability
        self.joker_frame = tk.Frame(self.prob_frame, bg='#16213e')
        self.joker_frame.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(self.joker_frame, text="🃏 JOKER", font=('Arial', 12, 'bold'), fg='#9C27B0', bg='#16213e', width=12, anchor='w').pack(side=tk.LEFT)
        self.joker_label = tk.Label(self.joker_frame, text="0.0%", font=('Arial', 14, 'bold'), fg='#ffffff', bg='#16213e')
        self.joker_label.pack(side=tk.RIGHT)
        self.joker_bar = tk.Canvas(self.prob_frame, height=20, bg='#0d0d1a', highlightthickness=0)
        self.joker_bar.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.is_open = True
        self.update()
    
    def close(self):
        if self.window:
            self.window.destroy()
            self.window = None
        self.is_open = False
    
    def update(self):
        if not self.is_open or not self.window:
            return
        
        probs = self.game.calculate_probabilities()
        
        self.higher_label.config(text=f"{probs['higher']:.1f}%")
        self.same_label.config(text=f"{probs['same']:.1f}%")
        self.lower_label.config(text=f"{probs['lower']:.1f}%")
        self.joker_label.config(text=f"{probs['joker']:.1f}%")
        
        # Update bars
        self._draw_bar(self.higher_bar, probs['higher'], '#4CAF50')
        self._draw_bar(self.same_bar, probs['same'], '#2196F3')
        self._draw_bar(self.lower_bar, probs['lower'], '#f44336')
        self._draw_bar(self.joker_bar, probs['joker'], '#9C27B0')
    
    def _draw_bar(self, canvas, percentage, color):
        canvas.delete("all")
        canvas.update_idletasks()
        width = canvas.winfo_width()
        if width > 1:
            bar_width = (percentage / 100) * width
            canvas.create_rectangle(0, 0, bar_width, 20, fill=color, outline='')


class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Higher / Lower Card Game")
        self.root.geometry("700x900")
        self.root.resizable(False, False)
        self.root.configure(bg='#1a1a2e')
        
        self.game = Game()
        self.leaderboard = Leaderboard()
        self.animation_running = False
        self.game_started = False
        self.awaiting_joker_guess = False
        
        self.setup_ui()
        self.setup_keyboard_bindings()
        self.prob_panel = ProbabilityPanel(self.root, self.game)
        self.show_menu()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_keyboard_bindings(self):
        self.root.bind('<Right>', lambda e: self.make_guess('higher'))
        self.root.bind('<Left>', lambda e: self.make_guess('lower'))
        self.root.bind('<Down>', lambda e: self.make_guess('same'))
        self.root.bind('<p>', lambda e: self.toggle_probability_panel())
        self.root.bind('<P>', lambda e: self.toggle_probability_panel())
        self.root.bind('<Escape>', lambda e: self.handle_escape())
    
    def handle_escape(self):
        if self.game_started:
            self.show_menu()
        else:
            self.on_closing()
    
    def toggle_probability_panel(self):
        if self.game_started:
            self.prob_panel.toggle()
    
    def setup_ui(self):
        self.main_frame = tk.Frame(self.root, bg='#1a1a2e')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = tk.Label(self.main_frame, text="HIGHER / LOWER", font=('Arial', 32, 'bold'), fg='#00d4ff', bg='#1a1a2e')
        title_label.pack(pady=(0, 10))
        
        # Controls hint
        self.controls_label = tk.Label(self.main_frame, text="← Lower | ↓ Same | → Higher | P: Odds", font=('Arial', 10), fg='#666666', bg='#1a1a2e')
        self.controls_label.pack(pady=(0, 10))
        
        self.stats_frame = tk.Frame(self.main_frame, bg='#16213e', relief=tk.RAISED, bd=2)
        
        stats_inner = tk.Frame(self.stats_frame, bg='#16213e')
        stats_inner.pack(padx=20, pady=15)
        
        self.score_label = tk.Label(stats_inner, text="Score: 0", font=('Arial', 18, 'bold'), fg='#ffd700', bg='#16213e')
        self.score_label.grid(row=0, column=0, padx=20)
        
        self.streak_label = tk.Label(stats_inner, text="Streak: 0", font=('Arial', 18, 'bold'), fg='#00ff88', bg='#16213e')
        self.streak_label.grid(row=0, column=1, padx=20)
        
        self.multiplier_label = tk.Label(stats_inner, text="Multiplier: 1x", font=('Arial', 18, 'bold'), fg='#ff6b9d', bg='#16213e')
        self.multiplier_label.grid(row=0, column=2, padx=20)
        
        self.cards_label = tk.Label(stats_inner, text="Cards: 53", font=('Arial', 14), fg='#a0a0a0', bg='#16213e')
        self.cards_label.grid(row=1, column=0, columnspan=3, pady=(10, 0))
        
        # Power-ups display
        self.powerups_frame = tk.Frame(self.main_frame, bg='#1a1a2e')
        self.shield_label = tk.Label(self.powerups_frame, text="🛡️ SHIELD", font=('Arial', 12, 'bold'), fg='#333333', bg='#1a1a2e')
        self.shield_label.pack(side=tk.LEFT, padx=20)
        self.double_label = tk.Label(self.powerups_frame, text="⚡ 2x NEXT", font=('Arial', 12, 'bold'), fg='#333333', bg='#1a1a2e')
        self.double_label.pack(side=tk.LEFT, padx=20)
        
        self.card_section = tk.Frame(self.main_frame, bg='#1a1a2e')
        
        self.card_display = tk.Frame(self.card_section, bg='#ffffff', width=200, height=280, relief=tk.RAISED, bd=3)
        self.card_display.pack_propagate(False)
        self.card_display.pack()
        
        self.card_rank_label = tk.Label(self.card_display, text="", font=('Arial', 72, 'bold'), bg='#ffffff')
        self.card_rank_label.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
        
        self.card_suit_label = tk.Label(self.card_display, text="", font=('Arial', 48), bg='#ffffff')
        self.card_suit_label.place(relx=0.5, rely=0.65, anchor=tk.CENTER)
        
        self.message_label = tk.Label(self.main_frame, text="", font=('Arial', 16, 'bold'), fg='#ffffff', bg='#1a1a2e', height=2, wraplength=600)
        
        self.game_buttons_frame = tk.Frame(self.main_frame, bg='#1a1a2e')
        
        button_style = {'font': ('Arial', 16, 'bold'), 'width': 10, 'height': 2, 'relief': tk.RAISED, 'bd': 3, 'cursor': 'hand2'}
        
        self.higher_btn = tk.Button(self.game_buttons_frame, text="HIGHER →", command=lambda: self.make_guess('higher'), bg='#4CAF50', fg='white', activebackground='#45a049', **button_style)
        self.higher_btn.grid(row=0, column=0, padx=10, pady=5)
        
        self.same_btn = tk.Button(self.game_buttons_frame, text="SAME ↓", command=lambda: self.make_guess('same'), bg='#2196F3', fg='white', activebackground='#1976D2', **button_style)
        self.same_btn.grid(row=0, column=1, padx=10, pady=5)
        
        self.lower_btn = tk.Button(self.game_buttons_frame, text="← LOWER", command=lambda: self.make_guess('lower'), bg='#f44336', fg='white', activebackground='#da190b', **button_style)
        self.lower_btn.grid(row=0, column=2, padx=10, pady=5)
        
        # Bottom buttons row
        bottom_buttons = tk.Frame(self.game_buttons_frame, bg='#1a1a2e')
        bottom_buttons.grid(row=1, column=0, columnspan=3, pady=(10, 0))
        
        self.view_cards_btn = tk.Button(bottom_buttons, text="View Remaining", command=self.show_remaining_cards, font=('Arial', 10, 'bold'), bg='#FF9800', fg='white', activebackground='#F57C00', width=14, height=2, relief=tk.RAISED, bd=3, cursor='hand2')
        self.view_cards_btn.pack(side=tk.LEFT, padx=5)
        
        self.odds_btn = tk.Button(bottom_buttons, text="Odds (P)", command=self.toggle_probability_panel, font=('Arial', 10, 'bold'), bg='#9C27B0', fg='white', activebackground='#7B1FA2', width=14, height=2, relief=tk.RAISED, bd=3, cursor='hand2')
        self.odds_btn.pack(side=tk.LEFT, padx=5)
        
        self.menu_frame = tk.Frame(self.main_frame, bg='#1a1a2e')
        
        menu_button_style = {'font': ('Arial', 16, 'bold'), 'width': 20, 'height': 3, 'relief': tk.RAISED, 'bd': 4, 'cursor': 'hand2'}
        
        self.new_game_menu_btn = tk.Button(self.menu_frame, text="NEW GAME", command=self.start_new_game, bg='#4CAF50', fg='white', activebackground='#45a049', **menu_button_style)
        self.new_game_menu_btn.pack(pady=15)
        
        self.leaderboard_btn = tk.Button(self.menu_frame, text="LEADERBOARD", command=self.show_leaderboard, bg='#FF9800', fg='white', activebackground='#F57C00', **menu_button_style)
        self.leaderboard_btn.pack(pady=15)
        
        self.quit_menu_btn = tk.Button(self.menu_frame, text="QUIT", command=self.on_closing, bg='#607D8B', fg='white', activebackground='#455A64', **menu_button_style)
        self.quit_menu_btn.pack(pady=15)
        
        self.game_over_frame = tk.Frame(self.main_frame, bg='#1a1a2e')
        
        game_over_title = tk.Label(self.game_over_frame, text="GAME OVER", font=('Arial', 36, 'bold'), fg='#ffd700', bg='#1a1a2e')
        game_over_title.pack(pady=20)
        
        self.final_score_label = tk.Label(self.game_over_frame, text="", font=('Arial', 24, 'bold'), fg='#00ff88', bg='#1a1a2e')
        self.final_score_label.pack(pady=10)
        
        self.final_streak_label = tk.Label(self.game_over_frame, text="", font=('Arial', 20), fg='#ff6b9d', bg='#1a1a2e')
        self.final_streak_label.pack(pady=10)
        
        self.name_entry_frame = tk.Frame(self.game_over_frame, bg='#1a1a2e')
        
        tk.Label(self.name_entry_frame, text="Enter your name:", font=('Arial', 16, 'bold'), fg='#00d4ff', bg='#1a1a2e').pack(pady=10)
        
        self.name_entry = tk.Entry(self.name_entry_frame, font=('Arial', 16), width=20, justify='center')
        self.name_entry.pack(pady=10)
        self.name_entry.bind('<Return>', lambda e: self.submit_score())
        
        submit_btn = tk.Button(self.name_entry_frame, text="SUBMIT SCORE", command=self.submit_score, font=('Arial', 14, 'bold'), bg='#4CAF50', fg='white', activebackground='#45a049', width=15, height=2, relief=tk.RAISED, bd=3, cursor='hand2')
        submit_btn.pack(pady=10)
        
        game_over_buttons = tk.Frame(self.game_over_frame, bg='#1a1a2e')
        game_over_buttons.pack(pady=30)
        
        self.play_again_btn = tk.Button(game_over_buttons, text="PLAY AGAIN", command=self.start_new_game, font=('Arial', 16, 'bold'), bg='#4CAF50', fg='white', activebackground='#45a049', width=15, height=3, relief=tk.RAISED, bd=4, cursor='hand2')
        self.play_again_btn.pack(side=tk.LEFT, padx=10)
        
        self.main_menu_btn = tk.Button(game_over_buttons, text="MAIN MENU", command=self.show_menu, font=('Arial', 16, 'bold'), bg='#FF9800', fg='white', activebackground='#F57C00', width=15, height=3, relief=tk.RAISED, bd=4, cursor='hand2')
        self.main_menu_btn.pack(side=tk.LEFT, padx=10)
    
    def show_menu(self):
        self.game_started = False
        self.awaiting_joker_guess = False
        self.stats_frame.pack_forget()
        self.powerups_frame.pack_forget()
        self.card_section.pack_forget()
        self.message_label.pack_forget()
        self.game_buttons_frame.pack_forget()
        self.game_over_frame.pack_forget()
        self.controls_label.pack_forget()
        
        self.prob_panel.close()
        
        self.card_rank_label.config(text="?", fg='#cccccc')
        self.card_suit_label.config(text="")
        
        self.menu_frame.pack(pady=30)
    
    def show_game_screen(self):
        self.menu_frame.pack_forget()
        self.game_over_frame.pack_forget()
        
        self.controls_label.pack(pady=(0, 10))
        self.stats_frame.pack(fill=tk.X, pady=(0, 10))
        self.powerups_frame.pack(pady=(0, 10))
        self.card_section.pack(pady=15)
        self.message_label.pack(pady=10)
        self.game_buttons_frame.pack(pady=15)
        
        self.update_display()
        self.update_powerups_display()
        self.enable_game_buttons()
        self.message_label.config(text="Make your guess!", fg='#ffffff')
    
    def update_powerups_display(self):
        if self.game.has_shield:
            self.shield_label.config(fg='#4CAF50')
        else:
            self.shield_label.config(fg='#333333')
        
        if self.game.double_or_nothing_active:
            self.double_label.config(fg='#ffd700')
        else:
            self.double_label.config(fg='#333333')
    
    def start_new_game(self):
        if self.animation_running:
            return
        
        self.game.reset()
        self.game.start()
        self.game_started = True
        self.awaiting_joker_guess = False
        
        self.show_game_screen()
    
    def make_guess(self, guess: str):
        if self.animation_running or not self.game_started or self.game.is_over:
            return
        
        if not self.game.deck.has_cards():
            self.end_game("Deck is empty!")
            return
        
        self.disable_game_buttons()
        self.animation_running = True
        
        is_correct, next_card, joker_type = self.game.make_guess(guess)
        
        if next_card is None:
            self.animation_running = False
            self.end_game("Deck is empty!")
            return
        
        self.animate_card_flip(next_card, is_correct, joker_type)
    
    def animate_card_flip(self, next_card, is_correct: bool, joker_type: Optional[str]):
        self.card_display.config(bg='#ffeb3b')
        self.card_rank_label.config(text="?", fg='#666666')
        self.card_suit_label.config(text="")
        
        self.root.after(300, lambda: self.reveal_card(next_card, is_correct, joker_type))
    
    def reveal_card(self, next_card, is_correct: bool, joker_type: Optional[str]):
        self.card_display.config(bg='#ffffff')
        self.card_rank_label.config(text=next_card.rank if not next_card.is_joker else "🃏", fg=next_card.get_color())
        self.card_suit_label.config(text=next_card.get_symbol() if not next_card.is_joker else "", fg=next_card.get_color())
        
        self.update_stats()
        self.update_powerups_display()
        self.prob_panel.update()
        
        if joker_type == 'shield':
            self.message_label.config(text="🃏 JOKER! You got a SHIELD!\nNext wrong guess won't end the game. Make your next guess!", fg='#9C27B0')
            self.flash_success()
            self.root.after(500, lambda: self.continue_after_joker())
        elif joker_type == 'double':
            self.message_label.config(text="🃏 JOKER! DOUBLE OR NOTHING!\nWin = 2x score, Lose = ½ score + game over. Make your guess!", fg='#ffd700')
            self.flash_success()
            self.root.after(500, lambda: self.continue_after_joker())
        elif joker_type == 'shield_used':
            self.message_label.config(text="🛡️ SHIELD ACTIVATED! Wrong guess, but you're safe!\nStreak reset. Keep playing!", fg='#FF9800')
            self.flash_failure()
            self.root.after(800, lambda: self.complete_turn(True))
        elif is_correct:
            if self.game.double_or_nothing_active:
                self.message_label.config(text=f"🎉 DOUBLE OR NOTHING WIN! Score doubled!", fg='#ffd700')
            else:
                multiplier = self.game.get_multiplier()
                self.message_label.config(text=f"Correct! +{multiplier} points", fg='#00ff88')
            self.flash_success()
            self.root.after(500, lambda: self.complete_turn(is_correct))
        else:
            if self.game.score > 0:
                self.message_label.config(text=f"💥 DOUBLE OR NOTHING LOSS! Score halved to {self.game.score}. Game Over!", fg='#ff6b6b')
            else:
                self.message_label.config(text="Wrong! Game Over", fg='#ff6b6b')
            self.flash_failure()
            self.root.after(500, lambda: self.complete_turn(is_correct))
    
    def continue_after_joker(self):
        self.animation_running = False
        self.awaiting_joker_guess = True
        self.enable_game_buttons()
    
    def complete_turn(self, is_correct: bool):
        self.animation_running = False
        self.awaiting_joker_guess = False
        
        if is_correct and not self.game.is_over:
            if self.game.deck.has_cards():
                self.enable_game_buttons()
                if not self.game.double_or_nothing_active:
                    self.message_label.config(text="Make your guess!", fg='#ffffff')
            else:
                self.end_game("Deck complete! Amazing!")
        else:
            self.end_game(None)
    
    def flash_success(self):
        original_bg = self.root.cget('bg')
        self.root.config(bg='#1b4332')
        self.root.after(200, lambda: self.root.config(bg=original_bg))
    
    def flash_failure(self):
        original_bg = self.root.cget('bg')
        self.root.config(bg='#4a1616')
        self.root.after(200, lambda: self.root.config(bg=original_bg))
    
    def end_game(self, message: Optional[str]):
        self.game_started = False
        self.disable_game_buttons()
        self.prob_panel.close()
        
        if message:
            self.message_label.config(text=message, fg='#ffd700')
        
        self.root.after(1000, lambda: self.handle_game_over())
    
    def handle_game_over(self):
        self.final_score_label.config(text=f"Final Score: {self.game.score}")
        self.final_streak_label.config(text=f"Final Streak: {self.game.streak}")
        
        self.stats_frame.pack_forget()
        self.powerups_frame.pack_forget()
        self.card_section.pack_forget()
        self.message_label.pack_forget()
        self.game_buttons_frame.pack_forget()
        self.controls_label.pack_forget()
        
        if self.leaderboard.is_high_score(self.game.score):
            self.name_entry_frame.pack(pady=20)
            self.name_entry.delete(0, tk.END)
            self.name_entry.focus()
        else:
            self.name_entry_frame.pack_forget()
        
        self.game_over_frame.pack(pady=30)
    
    def submit_score(self):
        player_name = self.name_entry.get().strip()[:20]
        if not player_name:
            player_name = "Anonymous"
        
        self.leaderboard.add_score(player_name, self.game.score, self.game.streak)
        self.name_entry_frame.pack_forget()
        messagebox.showinfo("Score Submitted", f"Score saved for {player_name}!", parent=self.root)
    
    def show_remaining_cards(self):
        if not self.game_started or self.animation_running:
            return
        
        remaining = self.game.get_remaining_cards()
        RemainingCardsWindow(self.root, remaining)
    
    def show_leaderboard(self):
        LeaderboardWindow(self.root, self.leaderboard)
    
    def update_display(self):
        if self.game.current_card:
            self.card_display.config(bg='#ffffff')
            if self.game.current_card.is_joker:
                self.card_rank_label.config(text="🃏", fg=self.game.current_card.get_color())
                self.card_suit_label.config(text="", fg=self.game.current_card.get_color())
            else:
                self.card_rank_label.config(text=self.game.current_card.rank, fg=self.game.current_card.get_color())
                self.card_suit_label.config(text=self.game.current_card.get_symbol(), fg=self.game.current_card.get_color())
        
        self.update_stats()
        self.prob_panel.update()
    
    def update_stats(self):
        self.score_label.config(text=f"Score: {self.game.score}")
        self.streak_label.config(text=f"Streak: {self.game.streak}")
        self.multiplier_label.config(text=f"Multiplier: {self.game.get_multiplier()}x")
        self.cards_label.config(text=f"Cards: {len(self.game.deck.cards)}")
    
    def enable_game_buttons(self):
        self.higher_btn.config(state=tk.NORMAL)
        self.same_btn.config(state=tk.NORMAL)
        self.lower_btn.config(state=tk.NORMAL)
        self.view_cards_btn.config(state=tk.NORMAL)
        self.odds_btn.config(state=tk.NORMAL)
    
    def disable_game_buttons(self):
        self.higher_btn.config(state=tk.DISABLED)
        self.same_btn.config(state=tk.DISABLED)
        self.lower_btn.config(state=tk.DISABLED)
        self.view_cards_btn.config(state=tk.DISABLED)
        self.odds_btn.config(state=tk.DISABLED)
    
    def on_closing(self):
        self.prob_panel.close()
        if self.game_started and not self.game.is_over:
            if messagebox.askokcancel("Quit", "Game in progress. Are you sure you want to quit?"):
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    root = tk.Tk()
    app = GameGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
