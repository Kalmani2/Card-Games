# Card Games (Higher / Lower)

This project is an extended version of a Higher / Lower card game written in Python. I started by building a small game engine that models cards, a deck, and the game rules, and then layered a Tkinter GUI on top of it. The game logic is kept separate from the interface so rules and features can change without affecting the UI.

The core game uses a standard 52-card deck, supports shuffling, and implements Higher, Lower, and Same guesses. Ace is treated as the highest card, and a streak-based multiplier system rewards consistent correct guesses.

## Structure and design

The structure is intentionally simple. Cards and decks are modelled as their own objects, while all game state such as score, streaks, jokers, and end conditions lives in a single game controller. The GUI layer handles input and display only and contains no game logic.

## User interface

The interface is built using Tkinter as a lightweight and familiar choice that allowed me to focus on behaviour rather than tooling. The game runs entirely in one window, with a clear flow from menu to gameplay and into the game-over state. Modal popups are avoided during play to keep the experience predictable.

## Jokers and gameplay extensions

As an extension, I added two jokers directly into the deck and made them meaningfully affect gameplay. One joker acts as a shield, allowing a single incorrect guess without immediately ending the game, while the other introduces a high-risk decision by doubling the score on success but halving it and ending the game on failure.

## Odds and transparency

An optional odds panel calculates the real probabilities of Higher, Lower, Same, and Joker outcomes based on the current card and remaining deck. This reflects the actual deck state and allows the player to make informed decisions rather than guessing blindly.

## Leaderboard

A simple persistent leaderboard is stored in a local JSON file. After each game, the score and streak are checked against existing entries, and high scores are recorded with a name to give the game replay value across sessions.

## Controls

The game supports keyboard controls in addition to buttons for faster play:

- Left Arrow: Lower  
- Right Arrow: Higher  
- Down Arrow: Same  
- P: Toggle odds panel  
- Escape: Return to menu during a game  

## Running the game

### Requirements

- Python 3.x

### Run

From the project directory:

```bash
python higher_lower_gui.py
````

## Possible improvements

With more time, I would add an alternative game mode using the same card and deck logic, expand the joker system with additional effects, and improve visual feedback for special states. The existing structure was designed to support these kinds of extensions without having to refacor it too much.

