# import random
# import tkinter as tk
# from tkinter import messagebox, simpledialog, Button, Label, Toplevel, ScrolledText, ttk
# import datetime
# import nltk
# from nltk.corpus import words
# import wikipedia
# import requests
# import json
# from typing import List, Set, Dict
# import threading
# import time

# nltk.download('words')

# class WordGameEngine:
#     def __init__(self):
#         self.leaderboard: List[tuple] = []
#         self.difficulty_config = {
#             'easy': {'min_len': 4, 'max_len': 6, 'hints': 5, 'reveal_last': False},
#             'hard': {'min_len': 7, 'max_len': 9, 'hints': 3, 'reveal_last': True},
#             'evil': {'min_len': 10, 'max_len': 15, 'hints': 2, 'reveal_last': True}
#         }
#         self.current_streaks: Dict[str, int] = {}
#         self.achievement_rules = {
#             'quick_solver': {'desc': 'Solved within 30 seconds', 'points': 50},
#             'no_hints': {'desc': 'Solved without using hints', 'points': 100},
#             'perfect_game': {'desc': 'No wrong guesses', 'points': 150},
#             'streak_bonus': {'desc': 'Win streak bonus', 'points': 25}
#         }

#     def choose_word(self, difficulty: str) -> str:
#         config = self.difficulty_config[difficulty]
#         word_list = [w.lower() for w in words.words() 
#                     if config['min_len'] <= len(w) <= config['max_len']]
#         return random.choice(word_list)

#     def calculate_score(self, base_score: int, time_taken: float, hints_used: int, 
#                        wrong_guesses: int, streak: int) -> tuple:
#         achievements = []
#         bonus = 0

#         if time_taken < 30:
#             achievements.append(('quick_solver', 50))
#             bonus += 50
#         if hints_used == 0:
#             achievements.append(('no_hints', 100))
#             bonus += 100
#         if wrong_guesses == 0:
#             achievements.append(('perfect_game', 150))
#             bonus += 150
#         if streak > 1:
#             streak_bonus = min(streak * 25, 100)
#             achievements.append(('streak_bonus', streak_bonus))
#             bonus += streak_bonus

#         return base_score + bonus, achievements

# class WordGameUI(tk.Tk):
#     def __init__(self, game_engine: WordGameEngine):
#         super().__init__()
#         self.engine = game_engine
#         self.setup_window()
#         self.create_styles()
        
#     def setup_window(self):
#         self.title("🎮 Educational Word Discovery")
#         self.geometry("1400x900")
#         self.configure(bg="#1a1a2e")
#         self.grid_columnconfigure(0, weight=1)
#         self.grid_rowconfigure(0, weight=1)

#     def create_styles(self):
#         style = ttk.Style()
#         style.configure('GameButton.TButton', 
#                        font=('Helvetica', 14),
#                        padding=10,
#                        background='#0f3460')
#         style.configure('Title.TLabel',
#                        font=('Helvetica', 36, 'bold'),
#                        foreground='#e94560',
#                        background='#1a1a2e')

#     def show_main_menu(self):
#         self.clear_window()
        
#         main_frame = tk.Frame(self, bg="#1a1a2e")
#         main_frame.pack(expand=True)

#         ttk.Label(
#             main_frame,
#             text="Educational Word Discovery",
#             style='Title.TLabel'
#         ).pack(pady=30)

#         difficulties = [
#             ("Easy Mode", "easy", "#4CAF50"),
#             ("Hard Mode", "hard", "#FF9800"),
#             ("Evil Mode", "evil", "#F44336")
#         ]

#         for name, diff, color in difficulties:
#             btn_frame = tk.Frame(main_frame, bg="#1a1a2e")
#             btn_frame.pack(pady=10)
            
#             btn = tk.Button(
#                 btn_frame,
#                 text=name,
#                 font=("Helvetica", 18),
#                 bg=color,
#                 width=20,
#                 command=lambda d=diff: self.start_game(d)
#             )
#             btn.pack(side=tk.LEFT, padx=10)

#             desc = self.get_difficulty_description(diff)
#             ttk.Label(
#                 btn_frame,
#                 text=desc,
#                 font=("Helvetica", 12),
#                 foreground='white',
#                 background='#1a1a2e'
#             ).pack(side=tk.LEFT, padx=10)

#     def get_difficulty_description(self, difficulty: str) -> str:
#         config = self.engine.difficulty_config[difficulty]
#         desc = f"{config['min_len']}-{config['max_len']} letters • {config['hints']} hints"
#         if config['reveal_last']:
#             desc += " • First & last letters shown"
#         else:
#             desc += " • First letter shown"
#         return desc

#     def start_game(self, difficulty: str):
#         player = self.get_player_name()
#         if not player:
#             return

#         if difficulty == 'evil':
#             self.show_evil_mode_rules()

#         game_session = GameSession(self, self.engine, difficulty, player)
#         game_session.run()

#     def get_player_name(self) -> str:
#         return simpledialog.askstring("Player Name", "Enter your name:", parent=self)

#     def show_evil_mode_rules(self):
#         rules = """
#         🔥 EVIL MODE RULES 🔥
        
#         1. Words are 10+ letters long
#         2. Only 2 hints available
#         3. First & last letters shown
#         4. No repeated hints
#         5. Double points for correct guesses
#         6. Triple penalties for wrong guesses
#         7. Time pressure: Score decreases over time
#         """
#         messagebox.showinfo("Evil Mode", rules)

#     def clear_window(self):
#         for widget in self.winfo_children():
#             widget.destroy()

# class GameSession:
#     def __init__(self, parent: WordGameUI, engine: WordGameEngine, 
#                  difficulty: str, player: str):
#         self.parent = parent
#         self.engine = engine
#         self.difficulty = difficulty
#         self.player = player
#         self.word = engine.choose_word(difficulty)
#         self.guessed_letters: Set[str] = set()
#         self.used_hints: Set[str] = set()
#         self.wrong_guesses = 0
#         self.hints_left = engine.difficulty_config[difficulty]['hints']
#         self.score = 100
#         self.start_time = time.time()
        
#         # Reveal appropriate letters
#         self.guessed_letters.add(self.word[0])
#         if engine.difficulty_config[difficulty]['reveal_last']:
#             self.guessed_letters.add(self.word[-1])

#         self.setup_ui()
#         self.start_timer()

#     def setup_ui(self):
#         self.parent.clear_window()
#         self.game_frame = tk.Frame(self.parent, bg="#1a1a2e")
#         self.game_frame.pack(expand=True, fill='both')

#         self.setup_info_panel()
#         self.setup_word_display()
#         self.setup_keyboard()
#         self.setup_hint_button()
#         self.update_display()

#     def setup_info_panel(self):
#         info_frame = tk.Frame(self.game_frame, bg="#1a1a2e")
#         info_frame.pack(pady=20)

#         labels = [
#             (f"Player: {self.player}", "#4CAF50"),
#             (f"Difficulty: {self.difficulty.title()}", "#FF9800"),
#             (f"Score: {self.score}", "#F44336")
#         ]

#         for text, color in labels:
#             Label(
#                 info_frame,
#                 text=text,
#                 font=("Helvetica", 16),
#                 bg="#1a1a2e",
#                 fg=color
#             ).pack(side=tk.LEFT, padx=20)

#         self.timer_label = Label(
#             info_frame,
#             text="Time: 0:00",
#             font=("Helvetica", 16),
#             bg="#1a1a2e",
#             fg="white"
#         )
#         self.timer_label.pack(side=tk.LEFT, padx=20)

#     def setup_word_display(self):
#         self.word_display = Label(
#             self.game_frame,
#             text="",
#             font=("Courier", 48, "bold"),
#             bg="#1a1a2e",
#             fg="white"
#         )
#         self.word_display.pack(pady=30)

#     def setup_keyboard(self):
#         keyboard_frame = tk.Frame(self.game_frame, bg="#1a1a2e")
#         keyboard_frame.pack(pady=20)

#         for row in ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']:
#             row_frame = tk.Frame(keyboard_frame, bg="#1a1a2e")
#             row_frame.pack(pady=5)
#             for letter in row:
#                 Button(
#                     row_frame,
#                     text=letter.upper(),
#                     font=("Helvetica", 18),
#                     width=4,
#                     bg="#0f3460",
#                     fg="white",
#                     command=lambda l=letter: self.guess_letter(l)
#                 ).pack(side=tk.LEFT, padx=3)

#     def setup_hint_button(self):
#         Button(
#             self.game_frame,
#             text=f"Get Hint ({self.hints_left} left) 💡",
#             font=("Helvetica", 14),
#             bg="#FFB74D",
#             command=self.get_hint
#         ).pack(pady=20)

#     def start_timer(self):
#         self.timer_thread = threading.Thread(target=self.update_timer, daemon=True)
#         self.timer_thread.start()

#     def update_timer(self):
#         while True:
#             elapsed = int(time.time() - self.start_time)
#             minutes = elapsed // 60
#             seconds = elapsed % 60
#             self.timer_label.config(text=f"Time: {minutes}:{seconds:02d}")
            
#             # Score decay in evil mode
#             if self.difficulty == 'evil' and elapsed % 10 == 0:
#                 self.score = max(0, self.score - 5)
#                 self.update_display()
            
#             time.sleep(1)

#     def guess_letter(self, letter: str):
#         if letter in self.guessed_letters:
#             return

#         self.guessed_letters.add(letter)
#         if letter in self.word:
#             self.score += 20 if self.difficulty == 'evil' else 10
#         else:
#             self.score -= 30 if self.difficulty == 'evil' else 10
#             self.wrong_guesses += 1

#         self.update_display()
#         self.check_game_status()

#     def get_hint(self):
#         if self.hints_left <= 0:
#             return

#         unguessed = [l for l in self.word 
#                     if l not in self.guessed_letters 
#                     and l not in self.used_hints]
        
#         if unguessed:
#             hint_letter = random.choice(unguessed)
#             self.guessed_letters.add(hint_letter)
#             self.used_hints.add(hint_letter)
#             self.hints_left -= 1
#             self.score -= 20
#             self.update_display()

#     def update_display(self):
#         word_display = ' '.join(
#             letter if letter in self.guessed_letters else '_' 
#             for letter in self.word
#         )
#         self.word_display.config(text=word_display)

#     def check_game_status(self):
#         if all(letter in self.guessed_letters for letter in self.word):
#             self.handle_victory()

#     def handle_victory(self):
#         time_taken = time.time() - self.start_time
#         final_score, achievements = self.engine.calculate_score(
#             self.score, time_taken, 
#             len(self.used_hints), 
#             self.wrong_guesses,
#             self.engine.current_streaks.get(self.player, 0) + 1
#         )
        
#         self.engine.current_streaks[self.player] = \
#             self.engine.current_streaks.get(self.player, 0) + 1
        
#         self.engine.leaderboard.append(
#             (self.player, final_score, datetime.datetime.now())
#         )
        
#         self.show_victory_screen(final_score, achievements)
#         self.show_word_info()

#     def show_victory_screen(self, final_score: int, achievements: List[tuple]):
#         victory_window = Toplevel(self.parent)
#         victory_window.title("Victory! 🎉")
#         victory_window.geometry("500x600")
#         victory_window.configure(bg="#1a1a2e")

#         Label(
#             victory_window,
#             text="Congratulations!",
#             font=("Helvetica", 24, "bold"),
#             bg="#1a1a2e",
#             fg="#e94560"
#         ).pack(pady=20)

#         stats_frame = tk.Frame(victory_window, bg="#1a1a2e")
#         stats_frame.pack(pady=20)

#         stats = [
#             (f"Word: {self.word.upper()}", "#4CAF50"),
#             (f"Base Score: {self.score}", "#FF9800"),
#             (f"Final Score: {final_score}", "#F44336"),
#             (f"Time: {int(time.time() - self.start_time)}s", "#2196F3")
#         ]

#         for text, color in stats:
#             Label(
#                 stats_frame,
#                 text=text,
#                 font=("Helvetica", 16),
#                 bg="#1a1a2e",
#                 fg=color
#             ).pack(pady=5)

#         if achievements:
#             Label(
#                 victory_window,
#                 text="Achievements 🏆",
#                 font=("Helvetica", 18, "bold"),
#                 bg="#1a1a2e",
#                 fg="#e94560"
#             ).pack(pady=20)

#             for achievement, points in achievements:
#                 Label(
#                     victory_window,
#                     text=f"{self.engine.achievement_rules[achievement]['desc']}: +{points}",
#                     font=("Helvetica", 14),
#                     bg="#1a1a2e",
#                     fg="white"
#                 ).pack(pady=5)

#     def show_word_info(self):
#         try:
#             wiki_summary = wikipedia.summary(self.word, sentences=2)
#             response = requests.get(
#                 f"https://api.dictionaryapi.dev/api/v2/entries/en/{self.word}"
#             )
            
#             if response.status_code == 200:
#                 dict_data = response.json()[0]
#                 meanings = dict_data.get('meanings', [])
                
#                 info_window = Toplevel(self.parent)
#                 info_window.title(f"Learn: {self.word.upper()}")
#                 info_window.geometry("600x800")
#                 info_window.configure(bg="#1a1a2e")
#                 text = ScrolledText(info_window, wrap=tk.WORD, font=("Helvetica", 12), bg="#1a1a2e", fg="white")
#                 text.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

#                 text.tag_configure("title", font=("Helvetica", 16, "bold"), foreground="#e94560")
#                 text.tag_configure("section", font=("Helvetica", 14, "bold"), foreground="#FF9800")
#                 text.tag_configure("content", foreground="white")

#                 text.insert(tk.END, f"Word: {self.word.upper()}\n\n", "title")
#                 text.insert(tk.END, "Overview:\n", "section")
#                 text.insert(tk.END, f"{wiki_summary}\n\n", "content")

#                 text.insert(tk.END, "Definitions:\n", "section")
#                 for meaning in meanings:
#                     part_of_speech = meaning.get('partOfSpeech', '')
#                     definitions = meaning.get('definitions', [])
                    
#                     text.insert(tk.END, f"\n{part_of_speech.title()}:\n", "section")
#                     for i, def_data in enumerate(definitions, 1):
#                         text.insert(tk.END, f"{i}. {def_data.get('definition')}\n", "content")
                        
#                         example = def_data.get('example')
#                         if example:
#                             text.insert(tk.END, f"   Example: {example}\n", "content")

#                 text.insert(tk.END, "\nSynonyms:\n", "section")
#                 synonyms = []
#                 for meaning in meanings:
#                     synonyms.extend(meaning.get('synonyms', []))
#                 text.insert(tk.END, ", ".join(synonyms[:10]), "content")

#                 text.configure(state='disabled')
            
#         except Exception as e:
#             messagebox.showinfo("Word Info", f"Word: {self.word}\nDefinition lookup failed.")

# def main():
#     nltk.download('words')
#     engine = WordGameEngine()
#     game = WordGameUI(engine)
#     game.show_main_menu()
#     game.mainloop()

# if __name__ == "__main__":
#     main()





import random
import tkinter as tk
from tkinter import messagebox, simpledialog, Button, Label, Toplevel, ttk
from tkinter.scrolledtext import ScrolledText
import datetime
import nltk
from nltk.corpus import words
import wikipedia
import requests
import json
from typing import List, Set, Dict
import threading
import time

nltk.download('words')

class WordGameEngine:
    def __init__(self):
        self.leaderboard: List[tuple] = []
        self.difficulty_config = {
            'easy': {'min_len': 4, 'max_len': 6, 'hints': 5, 'reveal_last': False, 'attempts': 12},
            'hard': {'min_len': 7, 'max_len': 9, 'hints': 3, 'reveal_last': True, 'attempts': 8},
            'evil': {'min_len': 10, 'max_len': 15, 'hints': 2, 'reveal_last': True, 'attempts': 6}
        }
        self.current_streaks: Dict[str, int] = {}
        self.achievement_rules = {
            'quick_solver': {'desc': 'Solved within 30 seconds', 'points': 50},
            'no_hints': {'desc': 'Solved without using hints', 'points': 100},
            'perfect_game': {'desc': 'Solved with 50%+ attempts remaining', 'points': 150},
            'streak_bonus': {'desc': 'Win streak bonus', 'points': 25},
            'last_chance': {'desc': 'Won with last attempt', 'points': 200}
        }

    def choose_word(self, difficulty: str) -> str:
        config = self.difficulty_config[difficulty]
        word_list = [w.lower() for w in words.words() 
                    if config['min_len'] <= len(w) <= config['max_len']]
        return random.choice(word_list)

    def calculate_score(self, base_score: int, time_taken: float, hints_used: int, 
                       wrong_guesses: int, streak: int) -> tuple:
        achievements = []
        bonus = 0

        if time_taken < 30:
            achievements.append(('quick_solver', 50))
            bonus += 50
        if hints_used == 0:
            achievements.append(('no_hints', 100))
            bonus += 100
        if wrong_guesses == 0:
            achievements.append(('perfect_game', 150))
            bonus += 150
        if streak > 1:
            streak_bonus = min(streak * 25, 100)
            achievements.append(('streak_bonus', streak_bonus))
            bonus += streak_bonus

        return base_score + bonus, achievements

    def get_simple_definition(self, word: str) -> str:
        try:
            response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
            if response.status_code == 200:
                data = response.json()[0]
                meaning = data['meanings'][0]
                definition = meaning['definitions'][0]['definition']
                return f"Simple meaning: {definition}"
            return "Definition not available"
        except:
            return "Definition not available"

class WordGameUI(tk.Tk):
    def __init__(self, game_engine: WordGameEngine):
        super().__init__()
        self.engine = game_engine
        self.setup_window()
        self.create_styles()
        
    def setup_window(self):
        self.title("🎮 Word Discovery Challenge")
        self.geometry("1400x900")
        self.configure(bg="#1a1a2e")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def create_styles(self):
        style = ttk.Style()
        style.configure('GameButton.TButton', 
                       font=('Helvetica', 14),
                       padding=10,
                       background='#0f3460')
        style.configure('Title.TLabel',
                       font=('Helvetica', 36, 'bold'),
                       foreground='#e94560',
                       background='#1a1a2e')

    def show_main_menu(self):
        self.clear_window()
        
        main_frame = tk.Frame(self, bg="#1a1a2e")
        main_frame.pack(expand=True)

        ttk.Label(
            main_frame,
            text="Word Discovery Challenge",
            style='Title.TLabel'
        ).pack(pady=30)

        difficulties = [
            ("Easy Mode", "easy", "#4CAF50", "12 attempts"),
            ("Hard Mode", "hard", "#FF9800", "8 attempts"),
            ("Evil Mode", "evil", "#F44336", "6 attempts")
        ]

        for name, diff, color, attempts in difficulties:
            btn_frame = tk.Frame(main_frame, bg="#1a1a2e")
            btn_frame.pack(pady=10)
            
            btn = tk.Button(
                btn_frame,
                text=f"{name} ({attempts})",
                font=("Helvetica", 18),
                bg=color,
                width=20,
                command=lambda d=diff: self.start_game(d)
            )
            btn.pack(side=tk.LEFT, padx=10)

            desc = self.get_difficulty_description(diff)
            ttk.Label(
                btn_frame,
                text=desc,
                font=("Helvetica", 12),
                foreground='white',
                background='#1a1a2e'
            ).pack(side=tk.LEFT, padx=10)

    def get_difficulty_description(self, difficulty: str) -> str:
        config = self.engine.difficulty_config[difficulty]
        desc = f"{config['min_len']}-{config['max_len']} letters • {config['hints']} hints"
        if config['reveal_last']:
            desc += " • First & last letters shown"
        else:
            desc += " • First letter shown"
        return desc

    def start_game(self, difficulty: str):
        player = self.get_player_name()
        if not player:
            return

        if difficulty == 'evil':
            self.show_evil_mode_rules()

        game_session = GameSession(self, self.engine, difficulty, player)
        game_session.run()

    def get_player_name(self) -> str:
        return simpledialog.askstring("Player Name", "Enter your name:", parent=self)

    def show_evil_mode_rules(self):
        rules = """
        🔥 EVIL MODE RULES 🔥
        
        1. Words are 10+ letters long
        2. Only 2 hints available
        3. First & last letters shown
        4. Only 6 attempts!
        5. Double points for correct guesses
        6. Triple penalties for wrong guesses
        7. Time pressure: Score decreases over time
        8. No second chances!
        """
        messagebox.showinfo("Evil Mode", rules)

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

class GameSession:
    def __init__(self, parent: WordGameUI, engine: WordGameEngine, difficulty: str, player: str):
        self.parent = parent
        self.engine = engine
        self.difficulty = difficulty
        self.player = player
        self.word = engine.choose_word(difficulty)
        self.guessed_letters: Set[str] = set()
        self.used_hints: Set[str] = set()
        self.wrong_guesses = 0
        self.hints_left = engine.difficulty_config[difficulty]['hints']
        self.score = 100
        self.start_time = time.time()
        self.attempts_left = engine.difficulty_config[difficulty]['attempts']
        self.attempts_label = None
        
        # Reveal appropriate letters
        self.guessed_letters.add(self.word[0])
        if engine.difficulty_config[difficulty]['reveal_last']:
            self.guessed_letters.add(self.word[-1])

    def run(self):
        self.setup_ui()
        self.start_timer()

    def setup_ui(self):
        self.parent.clear_window()
        self.game_frame = tk.Frame(self.parent, bg="#1a1a2e")
        self.game_frame.pack(expand=True, fill='both')

        self.setup_info_panel()
        self.setup_word_display()
        self.setup_keyboard()
        self.setup_hint_button()
        self.update_display()

    def setup_info_panel(self):
        info_frame = tk.Frame(self.game_frame, bg="#1a1a2e")
        info_frame.pack(pady=20)

        labels = [
            (f"Player: {self.player}", "#4CAF50"),
            (f"Difficulty: {self.difficulty.title()}", "#FF9800"),
            (f"Score: {self.score}", "#F44336"),
            (f"Attempts: {self.attempts_left}", "#E91E63")
        ]

        for text, color in labels:
            if "Attempts" in text:
                self.attempts_label = Label(
                    info_frame,
                    text=text,
                    font=("Helvetica", 16),
                    bg="#1a1a2e",
                    fg=color
                )
                self.attempts_label.pack(side=tk.LEFT, padx=20)
            else:
                Label(
                    info_frame,
                    text=text,
                    font=("Helvetica", 16),
                    bg="#1a1a2e",
                    fg=color
                ).pack(side=tk.LEFT, padx=20)

        self.timer_label = Label(
            info_frame,
            text="Time: 0:00",
            font=("Helvetica", 16),
            bg="#1a1a2e",
            fg="white"
        )
        self.timer_label.pack(side=tk.LEFT, padx=20)

    def setup_word_display(self):
        self.word_display = Label(
            self.game_frame,
            text="",
            font=("Courier", 48, "bold"),
            bg="#1a1a2e",
            fg="white"
        )
        self.word_display.pack(pady=30)

    def setup_keyboard(self):
        keyboard_frame = tk.Frame(self.game_frame, bg="#1a1a2e")
        keyboard_frame.pack(pady=20)

        for row in ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']:
            row_frame = tk.Frame(keyboard_frame, bg="#1a1a2e")
            row_frame.pack(pady=5)
            for letter in row:
                Button(
                    row_frame,
                    text=letter.upper(),
                    font=("Helvetica", 18),
                    width=4,
                    bg="#0f3460",
                    fg="white",
                    command=lambda l=letter: self.guess_letter(l)
                ).pack(side=tk.LEFT, padx=3)

    def setup_hint_button(self):
        Button(
            self.game_frame,
            text=f"Get Hint ({self.hints_left} left) 💡",
            font=("Helvetica", 14),
            bg="#FFB74D",
            command=self.get_hint
        ).pack(pady=20)

    def start_timer(self):
        self.timer_thread = threading.Thread(target=self.update_timer, daemon=True)
        self.timer_thread.start()

    def update_timer(self):
        while True:
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            self.timer_label.config(text=f"Time: {minutes}:{seconds:02d}")
            
            if self.difficulty == 'evil' and elapsed % 10 == 0:
                self.score = max(0, self.score - 5)
                
            time.sleep(1)

    def guess_letter(self, letter: str):
        if letter in self.guessed_letters or self.attempts_left <= 0:
            return

        self.guessed_letters.add(letter)
        if letter in self.word:
            self.score += 20 if self.difficulty == 'evil' else 10
        else:
            self.score -= 30 if self.difficulty == 'evil' else 10
            self.wrong_guesses += 1
            self.attempts_left -= 1
            self.attempts_label.config(text=f"Attempts: {self.attempts_left}")

        self.update_display()
        
        if self.attempts_left <= 0:
            self.handle_game_over()
        else:
            self.check_game_status()

    def update_display(self):
        word_display = ' '.join(
            letter if letter in self.guessed_letters else '_' 
            for letter in self.word
        )
        self.word_display.config(text=word_display)

    def check_game_status(self):
        if all(letter in self.guessed_letters for letter in self.word):
            self.handle_victory()

    def handle_game_over(self):
        definition = self.engine.get_simple_definition(self.word)
        messagebox.showinfo("Game Over", 
                          f"Out of attempts!\nThe word was: {self.word.upper()}\n\n{definition}")
        self.parent.show_main_menu()

    def handle_victory(self):
        time_taken = time.time() - self.start_time
        attempts_bonus = 1 if self.attempts_left > (self.engine.difficulty_config[self.difficulty]['attempts'] // 2) else 0
        last_attempt_bonus = 1 if self.attempts_left == 1 else 0
        
        final_score, achievements = self.engine.calculate_score(
            self.score, 
            time_taken, 
            len(self.used_hints),
            self.wrong_guesses,
            self.engine.current_streaks.get(self.player, 0) + 1
        )

        if attempts_bonus:
            achievements.append(('perfect_game', 150))
            final_score += 150
            
        if last_attempt_bonus:
            achievements.append(('last_chance', 200))
            final_score += 200

        definition = self.engine.get_simple_definition(self.word)
        
        self.show_victory_screen(final_score, achievements, definition)

    def show_victory_screen(self, final_score: int, achievements: List[tuple], definition: str):
        victory_window = Toplevel(self.parent)
        victory_window.title("Victory! 🎉")
        victory_window.geometry("500x600")
        victory_window.configure(bg="#1a1a2e")

        Label(
            victory_window,
            text="Congratulations!",
            font=("Helvetica", 24, "bold"),
            bg="#1a1a2e",
            fg="#e94560"
        ).pack(pady=20)

        stats_frame = tk.Frame(victory_window, bg="#1a1a2e")
        stats_frame.pack(pady=20)

        stats = [
            (f"Word: {self.word.upper()}", "#4CAF50"),
            (f"Base Score: {self.score}", "#FF9800"),
            (f"Final Score: {final_score}", "#F44336"),
            (f"Time: {int(time.time() - self.start_time)}s", "#2196F3"),
            (f"Attempts Left: {self.attempts_left}", "#E91E63")
        ]

        for text, color in stats:
            Label(
                stats_frame,
                text=text,
                font=("Helvetica", 16),
                bg="#1a1a2e",
                fg=color
            ).pack(pady=5)
            
        Label(
            victory_window,
            text=definition,
            font=("Helvetica", 14),
            bg="#1a1a2e",
            fg="#4CAF50",
            wraplength=400
        ).pack(pady=20)

        if achievements:
            Label(
                victory_window,
                text="Achievements 🏆",
                font=("Helvetica", 18, "bold"),
                bg="#1a1a2e",
                fg="#e94560"
            ).pack(pady=20)

            for achievement, points in achievements:
                Label(
                    victory_window,
                    text=f"{self.engine.achievement_rules[achievement]['desc']}: +{points}",
                    font=("Helvetica", 14),
                    bg="#1a1a2e",
                    fg="white"
                ).pack(pady=5)

        Button(
            victory_window,
            text="Play Again",
            font=("Helvetica", 16),
            bg="#4CAF50",
            fg="white",
            command=lambda: [victory_window.destroy(), self.parent.show_main_menu()]
        ).pack(pady=20)

    def get_hint(self):
        if self.hints_left <= 0 or self.attempts_left <= 0:
            return

        unguessed = [l for l in self.word 
                    if l not in self.guessed_letters 
                    and l not in self.used_hints]
        
        if unguessed:
            hint_letter = random.choice(unguessed)
            self.guessed_letters.add(hint_letter)
            self.used_hints.add(hint_letter)
            self.hints_left -= 1
            self.score -= 20
            self.update_display()
            
def main():
    nltk.download('words')
    engine = WordGameEngine()
    game = WordGameUI(engine)
    game.show_main_menu()
    game.mainloop()

if __name__ == "__main__":
    main()