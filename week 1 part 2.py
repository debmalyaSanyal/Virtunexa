import tkinter as tk                                                                                                                     
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import pyttsx3

# Game Configuration
CONFIG = {
    "title": "Epic Adventure: The Shattered Realm",
    "bg_image": "default_bg.png",  # Path to your single image file
    "font": ("Helvetica", 14),
    "message_font": ("Helvetica", 16, "bold"),
    "button_font": ("Helvetica", 12, "bold"),
    "button_bg": "#4CAF50",
    "button_hover_bg": "#45A049",
    "text_color": "darkblue",
    "wraplength": 800
}

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Use a female voice
engine.setProperty('rate', 150)  # Adjust speech rate

def speak(message):
    """Convert text to speech."""
    engine.say(message)
    engine.runAndWait()

file_path = "C:\Users\DEBMALYA\Desktop\adventure game\bg.webp"

def load_background_image(file_path):
    """Loads an image as a Tkinter-compatible PhotoImage."""
    image = Image.open(file_path)
    return ImageTk.PhotoImage(image)

# Initialize main window
root = tk.Tk()
root.title(CONFIG["title"])
root.state('zoomed')
root.resizable(True, True)

# Set the background image
try:
    bg_image = load_background_image(CONFIG["bg_image"])
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)
except Exception as e:
    messagebox.showerror("Error", f"Failed to load background image: {e}")
    root.destroy()

# Frame for message display
message_frame = tk.Frame(root, bg="white")
message_frame.pack(fill="both", padx=20, pady=(20, 10), expand=True)

# Label for displaying messages
message_label = tk.Label(
    message_frame,
    text="Welcome to the Shattered Realm!",
    font=CONFIG["message_font"],
    bg="white",
    fg=CONFIG["text_color"],
    wraplength=CONFIG["wraplength"],
    padx=10,
    pady=10
)
message_label.pack(pady=10, fill="both", expand=True)

# Frame for options (buttons)
options_frame = tk.Frame(root, bg="white")
options_frame.pack(fill="both", padx=20, pady=10, expand=True)

# Global variables
global_inventory = []
global_exp = 0
global_energy = 100
selected_character = ""
story_flags = {
    "village_story_heard": False,
    "forest_guardian_met": False,
    "ancient_rune_found": False,
    "mountain_gate_opened": False,
}

# Functions for core game mechanics
def display_message(message):
    """Display a message in the game window and speak it."""
    message_label.config(text=message)
    speak(message)

def clear_options():
    """Clear all buttons in the options frame."""
    for widget in options_frame.winfo_children():
        widget.destroy()

def update_storyline(new_story, next_action):
    """Update storyline with a new message and next steps."""
    display_message(new_story)
    clear_options()
    for text, command in next_action:
        button = tk.Button(
            options_frame,
            text=text,
            font=CONFIG["button_font"],
            bg=CONFIG["button_bg"],
            fg="white",
            command=command,
            padx=10,
            pady=5
        )
        button.pack(pady=5, fill="both")
        button.bind("<Enter>", lambda e, b=button: b.config(bg=CONFIG["button_hover_bg"]))
        button.bind("<Leave>", lambda e, b=button: b.config(bg=CONFIG["button_bg"]))

def add_exp(points):
    global global_exp
    global_exp += points
    display_message(f"You gained {points} EXP! Total EXP: {global_exp}")

def boost_energy(amount):
    global global_energy
    global_energy += amount
    if global_energy > 100:
        global_energy = 100
    display_message(f"Energy boosted by {amount}. Current Energy: {global_energy}%")

# Game scenario functions
def choose_character():
    """Allow the player to choose their character."""
    def set_character(character):
        global selected_character
        selected_character = character
        start_scenario()

    update_storyline(
        "Choose your hero:\n\nThe Warrior: Strong and brave, skilled with weapons.\nThe Mage: Wise and powerful, adept in magic.\nThe Thief: Quick and cunning, master of stealth.",
        [
            ("The Warrior", lambda: set_character("Warrior")),
            ("The Mage", lambda: set_character("Mage")),
            ("The Thief", lambda: set_character("Thief")),
        ]
    )

def start_scenario():
    """Let the player choose how they want to start the game."""
    update_storyline(
        f"Brave {selected_character}, your adventure begins!\n\nChoose your starting point:",
        [
            ("Wake up in the Village of Light", lambda: village(start=True)),
            ("Lost in the Forest of Whispers", lambda: forest(start=True)),
            ("Scaling the Mountains of Shadow", lambda: mountains(start=True)),
        ]
    )

def crossroads():
    """The central decision point of the game."""
    update_storyline(
        "You stand at the crossroads of the Shattered Realm. Where will you go?",
        [
            ("Enter the Forest of Whispers", forest),
            ("Travel to the Village of Light", village),
            ("Climb the Mountains of Shadow", mountains),
            ("Inspect the glowing rune circle", rune_circle),
            ("Check your inventory", check_inventory),
            ("Rest and recover strength", rest_at_crossroads),
        ]
    )

def rest_at_crossroads():
    boost_energy(20)
    add_exp(10)
    update_storyline(
        "You rest for a while, feeling your strength return. The world seems a little brighter.",
        [("Return to the crossroads", crossroads)]
    )

def forest(start=False):
    if start:
        update_storyline(
            "The whispers of the forest call to you. Strange shadows move between the trees.",
            [("Explore deeper", explore_deep_forest), ("Return to the crossroads", crossroads)]
        )

def explore_deep_forest():
    update_storyline(
        "An ancient guardian appears! Will you fight, flee, or seek wisdom?",
        [
            ("Fight", fight_guardian),
            ("Flee", crossroads),
            ("Try to reason with the guardian", reason_with_guardian),
            ("Search for hidden knowledge", search_for_knowledge)
        ]
    )

def fight_guardian():
    display_message("You fought bravely and won! The guardian bestows a shimmering relic upon you.")
    global_inventory.append("Shimmering Relic")
    add_exp(50)
    update_storyline(
        "You now possess the Shimmering Relic. It pulses with power and may unlock hidden paths.",
        [("Search the guardian's lair", guardian_lair), ("Return to the crossroads", crossroads)]
    )

def search_for_knowledge():
    update_storyline(
        "You find a hidden grove within the forest where ancient runes glow with wisdom.",
        [("Learn the secret of the runes", learn_rune_secret), ("Return to the crossroads", crossroads)]
    )

def learn_rune_secret():
    story_flags["ancient_rune_found"] = True
    add_exp(30)
    display_message("The runes reveal a powerful enchantment to dispel barriers of shadow.")
    crossroads()

def guardian_lair():
    update_storyline(
        "In the guardian's lair, you discover ancient scrolls and a glowing gemstone.",
        [("Take the gemstone", lambda: collect_item("Glowing Gemstone")),
         ("Read the scrolls", read_scrolls),
         ("Return to the crossroads", crossroads)]
    )

def collect_item(item):
    global_inventory.append(item)
    add_exp(20)
    display_message(f"You take the {item}.")
    crossroads()

def read_scrolls():
    add_exp(25)
    display_message("The scrolls speak of a lost city beyond the Mountains of Shadow, guarded by fierce creatures.")
    crossroads()

def reason_with_guardian():
    update_storyline(
        "The guardian listens to your words. Moved by your wisdom, it shares a secret about the Mountains of Shadow.",
        [("Return to the crossroads", crossroads)]
    )

def village(start=False):
    if start:
        update_storyline(
            "The village elder speaks of a powerful rune hidden deep in the forest.",
            [
                ("Speak with the elder", explore_village),
                ("Visit the village market", village_market),
                ("Investigate the ancient well", investigate_well),
                ("Set out for the crossroads", crossroads)
            ]
        )

def investigate_well():
    update_storyline(
        "You peer into the ancient well and hear whispers of forgotten times.",
        [("Climb down the well", descend_well), ("Return to the village", crossroads)]
    )

def descend_well():
    update_storyline(
        "You discover a hidden chamber beneath the well, filled with treasures and a mysterious portal.",
        [("Enter the portal", enter_portal), ("Return to the surface", crossroads)]
    )

def enter_portal():
    update_storyline(
        "The portal transports you to a realm of endless stars and ancient magic. You feel destiny pulling you onward.",
        [("Step into the light", final_battle), ("Return to the crossroads", crossroads)]
    )

def final_battle():
    add_exp(100)
    boost_energy(30)
    display_message("The final battle is at hand. Will you emerge victorious?")
    crossroads()

def explore_village():
    update_storyline(
        "The elder's eyes glow as he speaks of destiny. He tells you of a secret path in the mountains.",
        [("Thank the elder", crossroads)]
    )

def village_market():
    update_storyline(
        "You browse the market stalls. A mysterious vendor offers a strange talisman in exchange for a relic.",
        [
            ("Trade the Shimmering Relic for the talisman", trade_for_talisman),
            ("Browse other goods", browse_goods),
            ("Leave the market", crossroads)
        ]
    )

# Continuation of the Adventure Game

def browse_goods():
    """Explore the items available in the village market."""
    update_storyline(
        "The vendor shows you potions and enchanted arrows."
        " These items might aid you on your journey.",
        [
            ("Buy a health potion", lambda: collect_item("Health Potion")),
            ("Buy enchanted arrows", lambda: collect_item("Enchanted Arrows")),
            ("Return to the crossroads", crossroads),
        ]
    )

def trade_for_talisman():
    """Trade the Shimmering Relic for a Mystic Talisman."""
    if "Shimmering Relic" in global_inventory:
        global_inventory.remove("Shimmering Relic")
        global_inventory.append("Mystic Talisman")
        add_exp(50)
        display_message("You trade the relic for the Mystic Talisman. It hums with otherworldly energy.")
    else:
        display_message("You don't have the Shimmering Relic to trade.")
    crossroads()

def rune_circle():
    """Interact with the glowing rune circle."""
    if story_flags["ancient_rune_found"]:
        update_storyline(
            "You activate the rune circle with the enchantment you learned. A hidden passage opens!",
            [
                ("Enter the passage", final_battle),
                ("Return to the crossroads", crossroads),
            ]
        )
    else:
        update_storyline(
            "The rune circle glows faintly. You sense it holds great power, but you need more knowledge to unlock it.",
            [("Return to the crossroads", crossroads)]
        )

def check_inventory():
    """Display the player's current inventory, energy, and EXP."""
    inventory_list = "\n".join(global_inventory) if global_inventory else "Your inventory is empty."
    update_storyline(
        f"Your Inventory:\n{inventory_list}\n\nEnergy: {global_energy}%\nEXP: {global_exp}",
        [("Return to the crossroads", crossroads)]
    )

# Initialize the adventure
choose_character()

# Start the Tkinter main loop
root.mainloop()
