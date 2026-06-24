#!/usr/bin/env python3
import random
import sys
import os

# ANSI color codes
GREEN  = "\033[42m\033[30m"
YELLOW = "\033[43m\033[30m"
GRAY   = "\033[100m\033[37m"
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"

WORD_LIST = [
    "apple", "brave", "chart", "dance", "eagle", "fable", "grace", "haste",
    "ivory", "joust", "kneel", "lemon", "maple", "nurse", "ocean", "piano",
    "queen", "rivet", "solar", "tiger", "ultra", "vivid", "waltz", "xenon",
    "yacht", "zebra", "blast", "crisp", "draft", "elite", "flame", "gloom",
    "hyena", "inlet", "joker", "knack", "lusty", "magic", "nymph", "olive",
    "plank", "quirk", "raven", "shack", "taunt", "umbra", "venom", "wrath",
    "xylem", "yearn", "zonal", "amber", "blaze", "cliff", "drape", "ember",
    "frost", "graze", "hinge", "irony", "jazzy", "karma", "latch", "midst",
    "noble", "optic", "prowl", "quail", "rebel", "snare", "thyme", "udder",
    "vapor", "wheat", "exile", "yodel", "zesty", "abode", "bench", "chimp",
    "depot", "elope", "flint", "guild", "haunt", "icier", "jumpy", "knave",
    "lunar", "mirth", "nerve", "oxide", "pearl", "quark", "risky", "sting",
    "trout", "unify", "vicar", "wound", "expel", "yield", "zilch", "abyss",
    "brawl", "cello", "dirge", "ergot", "firth", "gruel", "heron", "index",
    "knelt", "libel", "mourn", "niche", "ozone", "prism", "quell",
    "robin", "scout", "tuner", "usurp", "verge", "winch", "expat", "yokel",
    "actor", "brush", "cabin", "derby", "envoy", "fungi", "glare", "hound",
    "input", "jewel", "kinky", "lanky", "melee", "nasty", "onset", "pixel",
    "quota", "rover", "silly", "talon", "uncut", "valve", "woken", "extol",
]
# deduplicate and keep only 5-letter words
WORD_LIST = list({w for w in WORD_LIST if len(w) == 5})

MAX_GUESSES = 6

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def color_tile(ch, state):
    if state == "green":
        return f"{GREEN} {ch.upper()} {RESET}"
    elif state == "yellow":
        return f"{YELLOW} {ch.upper()} {RESET}"
    else:
        return f"{GRAY} {ch.upper()} {RESET}"

def empty_tile():
    return f"{DIM}[   ]{RESET}"

def score_guess(guess, answer):
    result = ["gray"] * 5
    answer_chars = list(answer)
    # First pass: greens
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            result[i] = "green"
            answer_chars[i] = None
    # Second pass: yellows
    for i, g in enumerate(guess):
        if result[i] == "green":
            continue
        if g in answer_chars:
            result[i] = "yellow"
            answer_chars[answer_chars.index(g)] = None
    return result

def render_board(guesses, scores, answer_len=5):
    print()
    for row in range(MAX_GUESSES):
        if row < len(guesses):
            g, s = guesses[row], scores[row]
            tiles = "  ".join(color_tile(g[i], s[i]) for i in range(answer_len))
        else:
            tiles = "  ".join(empty_tile() for _ in range(answer_len))
        print(f"  {tiles}")
    print()

def render_keyboard(used_letters):
    rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    print()
    for row in rows:
        line = "  "
        for ch in row:
            state = used_letters.get(ch)
            if state == "green":
                line += f"{GREEN}{ch.upper()}{RESET} "
            elif state == "yellow":
                line += f"{YELLOW}{ch.upper()}{RESET} "
            elif state == "gray":
                line += f"{GRAY}{ch.upper()}{RESET} "
            else:
                line += f"{ch.upper()} "
        print(line)
    print()

def update_keyboard(used_letters, guess, score):
    priority = {"green": 3, "yellow": 2, "gray": 1}
    for ch, state in zip(guess, score):
        existing = used_letters.get(ch)
        if existing is None or priority[state] > priority[existing]:
            used_letters[ch] = state

def play():
    answer = random.choice(WORD_LIST)
    guesses, scores = [], []
    used_letters = {}
    valid_words = set(WORD_LIST)

    while True:
        clear()
        print(f"\n  {BOLD}WORDLE{RESET}  — guess the 5-letter word in {MAX_GUESSES} tries\n")
        render_board(guesses, scores)
        render_keyboard(used_letters)

        if guesses and scores[-1] == ["green"] * 5:
            attempts = len(guesses)
            print(f"  {GREEN} YOU WIN {RESET}  Solved in {BOLD}{attempts}{RESET} guess{'es' if attempts != 1 else ''}!\n")
            break

        if len(guesses) >= MAX_GUESSES:
            print(f"  Better luck next time! The word was {BOLD}{answer.upper()}{RESET}\n")
            break

        remaining = MAX_GUESSES - len(guesses)
        try:
            raw = input(f"  Guess ({remaining} left): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n  Bye!")
            sys.exit(0)

        if len(raw) != 5 or not raw.isalpha():
            input("  ⚠  Please enter a 5-letter word. Press Enter to continue...")
            continue

        score = score_guess(raw, answer)
        guesses.append(raw)
        scores.append(score)
        update_keyboard(used_letters, raw, score)

    again = input("  Play again? (y/n): ").strip().lower()
    if again == "y":
        play()

if __name__ == "__main__":
    play()
