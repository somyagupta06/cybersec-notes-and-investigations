

# Password Strength Checker

A beginner-friendly Python script that evaluates password strength using a set of basic security criteria and provides a simple strength rating.

## What It Does

The program takes a password as input and checks it against the following criteria:

- Minimum 8 characters
- Contains at least one uppercase letter
- Contains at least one lowercase letter
- Contains at least one digit
- Contains at least one special character
- Is not included in a small list of common/weak passwords

The program then assigns a strength rating based on how many character-type criteria are satisfied.

### Strength Rating

| Criteria Met | Rating |
|---:|---|
| 4 | Strong |
| 3 | Good |
| 2 | Weak |
| 0–1 | Very Weak |

Common passwords and passwords shorter than 8 characters are rejected before the strength score is calculated.

## Why This Matters

Weak and predictable passwords can make accounts more vulnerable to attacks such as brute-force and dictionary attacks.

This project demonstrates how basic password-policy checks can be automated using Python.

> **Note:** This is a simple rule-based learning project. It does not perform real-world password entropy estimation or determine whether a password has been compromised.

## Technologies Used

- Python 3
- Built-in string methods
- `any()`
- Conditional statements
- Loops
- Lists

## How to Run

Make sure Python 3 is installed.

Run the script from the terminal:

```bash
python3 passwordchecker.py
```

You will be prompted to enter a password, and the program will display its strength rating.

## Example Output
```
Hello , This is a password checker.
Enter a password of at least 8 characters.: Abcdef1!

Your password is strong.
```
- Another example:
```
Hello , This is a password checker.
Enter a password of at least 8 characters.: abcdefgh

Your password is very weak.
```
## What I Learned

While building this project, I practiced and learned:

- Using any() with generator expressions to check conditions across characters in a string instead of writing manual loops.
- Why variable names should not shadow Python built-ins. I initially used sum as a variable name, which overwrote access to Python's built-in sum() function.
- The difference between isalpha() (checks whether a character is a letter) and isupper() / islower() (checks specifically for uppercase or lowercase characters). Using the wrong method caused two of my criteria to overlap instead of being independent.
- The importance of testing a program with multiple inputs rather than relying on a single test case.
- How conditional statements can be used to build a simple rule-based scoring system.
## Limitations

This project is intentionally simple and was built to practice Python fundamentals.

Current limitations include:

- The common-password list is small and hardcoded.
- Strength is determined by counting criteria rather than measuring password entropy.
- The program does not check whether a password has appeared in known data breaches.
- A password that satisfies all four character-type criteria is classified as "Strong" even though real-world password strength depends on more factors.

These limitations are intentional for the scope of this beginner project.

## Possible Improvements

Future versions could include:

- A larger common-password database
- Entropy-based password strength estimation
- Command-line argument support
- A graphical user interface
- Additional password-pattern checks
## Project Purpose

This project is part of my journey toward using Python for cybersecurity and security automation.

The goal of this project was not to build a production-grade password security tool, but to strengthen my understanding of Python fundamentals through a practical cybersecurity-related problem.


### My verdict

**Use this README and don't touch the project further.** ✅

Especially keep this line:

> *The goal of this project was not to build a production-grade password security tool, but to strengthen my understanding of Python fundamentals through a practical cybersecurity-related problem.*

That tells a recruiter exactly why a relatively simple project exists in your portfolio.

Once you replace the README with this, **Project 01 is complete.** Then we move to the next item in the roadmap rather than endlessly polishing this one.
