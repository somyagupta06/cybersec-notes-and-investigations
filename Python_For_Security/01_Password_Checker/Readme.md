# Password Strength Checker

A Python script that checks password strength against multiple security criteria and gives feedback on how to improve it.

## What it does      

Takes a password as input and checks it against these criteria:
- Minimum 8 characters
- Contains an uppercase letter
- Contains a lowercase letter
- Contains a digit
- Contains a special character
- Not in a list of common/weak passwords

Based on how many criteria are met, it rates the password as **Strong**, **Good**, **Weak**, or **Very Weak**.

## Why this matters

Weak passwords are one of the most common entry points for attackers — brute-force and dictionary attacks specifically target passwords that are short, predictable, or reused. This script automates the kind of check a password policy would enforce.

## How to run

```bash
python3 passwordchecker.py
```

You'll be prompted to enter a password, and the script will print its strength rating.

## What I learned

- Using `any()` with generator expressions to check conditions across characters in a string, instead of writing manual loops
- Why variable names shouldn't shadow Python built-ins (initially named a variable `sum`, which overwrote the built-in `sum()` function)
- The difference between `isalpha()` (any letter) and `isupper()`/`islower()` (specifically upper/lowercase) — using the wrong one made two of my criteria overlap instead of being independent checks
- The importance of testing with multiple real inputs, not just one, to catch logic bugs

## Possible improvements

- Add entropy-based strength scoring instead of just criteria counting
- Expand the common password list (currently a short hardcoded list)
- Add a GUI or command-line argument support instead of interactive input
