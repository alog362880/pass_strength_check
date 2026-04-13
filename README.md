# Password Strength Checker

A lightweight desktop app built with Python and Tkinter that analyses password strength in real time — no internet connection or third-party libraries required.

---

## Features

- **Live strength analysis** — feedback updates as you type
- **Visual strength bar** — colour-coded from red (weak) to green (strong)
- **Entropy calculation** — measures true randomness in bits
- **Requirements checklist** — 6 pass/fail indicators with instant feedback
- **Improvement suggestions** — actionable tips to strengthen your password
- **Show / Hide toggle** — reveal or mask the password field
- **Clear button** — reset with one click

---

## Project Structure

```
password_checker/
│
├── main.py          # Entry point — launches the app
├── app.py           # Tkinter UI class (PasswordCheckerApp)
├── analyser.py      # Password logic: scoring, entropy, tips, checklist
└── constants.py     # Colours, score labels, and theme values
```

### File Responsibilities

| File | Description |
|---|---|
| `main.py` | Imports and runs `PasswordCheckerApp` |
| `app.py` | Builds the full Tkinter window and all widgets; calls `analyser.py` on every keystroke |
| `analyser.py` | Pure logic — no UI dependencies; returns a dict with `score`, `entropy`, `tips`, `checks`, and `length` |
| `constants.py` | Single source of truth for all colours and score metadata |

---

## Requirements

- Python 3.7 or higher
- Tkinter (included with Python on Windows and macOS)

### Installing Tkinter on Linux

```bash
sudo apt install python3-tk
```

---

## How to Run

1. Clone or download this repository.
2. Place all four files in the same folder.
3. Run:

```bash
python main.py
```

---

## How Scoring Works

The analyser awards points based on the following criteria:

| Criterion | Points |
|---|---|
| 8 or more characters | +1 |
| 12 or more characters | +1 |
| Uppercase and lowercase mixed | +1 |
| Contains numbers | +1 |
| Contains symbols | +1 |

The total score (0–5) maps to a strength label:

| Score | Label |
|---|---|
| 1 | Very Weak |
| 2 | Weak |
| 3 | Fair |
| 4 | Strong |
| 5 | Very Strong |

### Entropy

Entropy is calculated as:

```
entropy = length × log₂(pool_size)
```

Where `pool_size` is the number of distinct character types used (lowercase, uppercase, digits, symbols). Higher entropy means the password is harder to brute-force.

---

## Screenshots

> Run `python main.py` to see the app in action.

---

## License

This project is free to use and modify for personal or educational purposes.
