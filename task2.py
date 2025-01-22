import random
import webbrowser
import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, Button, Label, Toplevel
import datetime
import winsound
import nltk
from nltk.corpus import words
import wikipedia

# Ensure words are available
nltk.download('words')

# Function to choose a word based on difficulty
def choose_word(difficulty):
    word_list = words.words()
    if difficulty == 'easy':
        filtered_words = [word for word in word_list if 4 <= len(word) <= 6]
    elif difficulty == 'hard':
        filtered_words = [word for word in word_list if 7 <= len(word) <= 10]
    elif difficulty == 'evil':
        filtered_words = [word for word in word_list if len(word) > 9]
    else:
        filtered_words = word_list
    return random.choice(filtered_words).lower()

# Function to fetch the meaning of a word
def get_word_meaning(word):
    try:
        summary = wikipedia.summary(word, sentences=1)
        return summary
    except:
        return 'Meaning not available.'

# Function to display the guessed word
def display_word(word, guessed_letters):
    return ' '.join(letter if letter in guessed_letters else '_' for letter in word)

# Function to save game results to the leaderboard database
def save_game_result(player_name, word, attempts_left):
    conn = sqlite3.connect('hangman_history.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS history (player_name TEXT, word TEXT, attempts_left INTEGER, date_time TEXT)")
    cursor.execute("INSERT INTO history (player_name, word, attempts_left, date_time) VALUES (?, ?, ?, ?)",
                   (player_name, word, attempts_left, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

# Function to play a system sound
def play_sound(sound_type):
    if sound_type == "correct":
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
    elif sound_type == "incorrect":
        winsound.MessageBeep(winsound.MB_ICONHAND)
    elif sound_type == "game_over":
        winsound.MessageBeep()

# Main game function
def hangman():
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Enhanced Hangman")
    root.configure(bg="#FFE4E1")

    welcome_label = Label(root, text="\U0001F3B2 Welcome to Hangman! \U0001F60E", font=("Helvetica", 24, "bold"), bg="#FFCDD2", fg="#4A148C")
    welcome_label.pack(pady=20)

    def start_game(difficulty):
        player_name = simpledialog.askstring("Hangman", "Enter your name:")
        if not player_name:
            messagebox.showinfo("Hangman", "Name is required to play.")
            return

        word_to_guess = choose_word(difficulty)
        guessed_letters = set()
        attempts_left = 6 if difficulty == 'easy' else 8 if difficulty == 'hard' else 10
        hints_left = 5

        game_window = Toplevel(root)
        game_window.title("Hangman Game")
        game_window.configure(bg="#F3E5F5")

        def update_display():
            word_label.config(text=display_word(word_to_guess, guessed_letters))
            attempts_label.config(text=f"Attempts left: {attempts_left}")
            hints_label.config(text=f"Hints left: {hints_left}")

        def guess_letter(letter):
            nonlocal attempts_left
            guessed_letters.add(letter)
            if letter in word_to_guess:
                play_sound("correct")
            else:
                attempts_left -= 1
                play_sound("incorrect")
            update_display()
            if all(letter in guessed_letters for letter in word_to_guess):
                messagebox.showinfo("Hangman", f"Congratulations, {player_name}! You guessed the word: {word_to_guess}")
                save_game_result(player_name, word_to_guess, attempts_left)
                game_window.destroy()
            elif attempts_left == 0:
                meaning = get_word_meaning(word_to_guess)
                play_sound("game_over")
                messagebox.showinfo("Game Over", f"The word was: {word_to_guess}\nMeaning: {meaning}")
                save_game_result(player_name, word_to_guess, 0)
                game_window.destroy()

        def use_hint():
            nonlocal hints_left, attempts_left
            if hints_left > 0:
                hints_left -= 1
                attempts_left -= 1
                hint_type = hints_left % 3
                if hint_type == 0:
                    hint = f"Hint: The word starts with '{word_to_guess[0]}'"
                elif hint_type == 1:
                    hint = f"Hint: The word ends with '{word_to_guess[-1]}'"
                else:
                    hint = f"Hint: One of the middle letters is '{word_to_guess[len(word_to_guess) // 2]}'"
                messagebox.showinfo("Hint", hint)
                update_display()
            else:
                messagebox.showinfo("Hint", "No hints left.")

        word_label = Label(game_window, text=display_word(word_to_guess, guessed_letters), font=("Helvetica", 24), bg="#E1BEE7", fg="#311B92")
        word_label.pack(pady=10)

        attempts_label = Label(game_window, text=f"Attempts left: {attempts_left}", font=("Helvetica", 16), bg="#F3E5F5", fg="#880E4F")
        attempts_label.pack(pady=5)

        hints_label = Label(game_window, text=f"Hints left: {hints_left}", font=("Helvetica", 16), bg="#F3E5F5", fg="#880E4F")
        hints_label.pack(pady=5)

        button_frame = tk.Frame(game_window, bg="#F3E5F5")
        button_frame.pack(pady=10)

        for letter in "abcdefghijklmnopqrstuvwxyz":
            Button(button_frame, text=letter.upper(), font=("Helvetica", 14), bg="#FFCDD2", fg="#D32F2F", width=3, command=lambda l=letter: guess_letter(l)).grid(row=ord(letter) // 13, column=ord(letter) % 13, padx=2, pady=2)

        Button(game_window, text="\U0001F50E Use Hint", font=("Helvetica", 14, "bold"), bg="#C5CAE9", fg="#1A237E", command=use_hint).pack(pady=10)

        update_display()

    Button(root, text="\U0001F4A1 Easy Mode", font=("Helvetica", 18, "bold"), bg="#C8E6C9", fg="#2E7D32", command=lambda: start_game('easy')).pack(pady=10)
    Button(root, text="\U0001F525 Hard Mode", font=("Helvetica", 18, "bold"), bg="#FFCDD2", fg="#C62828", command=lambda: start_game('hard')).pack(pady=10)
    Button(root, text="\U0001F608 Evil Mode", font=("Helvetica", 18, "bold"), bg="#D1C4E9", fg="#4A148C", command=lambda: start_game('evil')).pack(pady=10)

    Button(root, text="\U0000274C Exit", font=("Helvetica", 18, "bold"), bg="#FFCDD2", fg="#B71C1C", command=root.destroy).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    hangman()
