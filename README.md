# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**Game Purpose:** This is a number guessing game where the player tries to guess a secret number within a specified range. After each guess, the game provides directional hints ("Too High" or "Too Low") to guide the player closer to the answer. The game tracks attempts, score, and difficulty levels (Easy, Normal, Hard). The AI-generated initial code had critical bugs that made the game unplayable.

**Bugs Found (3 major issues fixed):**

1. **Backwards Hints (Bug #1):** When a player guessed too high, the hint incorrectly said "Go HIGHER!" instead of "Go LOWER!" This made it impossible to win using logic. The root cause was swapped messages in the `check_guess()` function.

2. **Broken Difficulty Progression (Bug #3):** Hard mode had a range of 1-50 with 5 attempts, while Normal mode had 1-100 with 8 attempts. This made Hard difficulty actually EASIER than Normal! The ranges were backwards in the `get_range_for_difficulty()` function.

3. **Incomplete Game State Reset (Bug #2):** Clicking "New Game" didn't properly reset the score and guess history, so they carried over from the previous game. The New Game button also used hardcoded range (1, 100) instead of respecting difficulty.

**Fixes Applied:**

- **Fix #1 (Backwards Hints):** Refactored `check_guess()` into `logic_utils.py` and corrected the logic so that when `guess > secret` it returns "📉 Go LOWER!" and when `guess < secret` it returns "📈 Go HIGHER!"

- **Fix #2 (Game State Reset):** Updated the New Game button to explicitly reset `score = 0` and `history = []`, plus changed the range generation to use `random.randint(low, high)` to respect the current difficulty.

- **Fix #3 (Difficulty Configuration):** Corrected the difficulty progression:
  - Easy: 1-20 range, 6 attempts
  - Normal: 1-50 range, 8 attempts
  - Hard: 1-100 range, 5 attempts (now truly the hardest!)

- **Refactoring:** Moved all game logic (`get_range_for_difficulty()`, `parse_guess()`, `check_guess()`, `update_score()`) into `logic_utils.py` and updated imports in `app.py`.

- **Testing:** Created 14 comprehensive pytest tests with specific bug-fix validation tests that all pass.

## 📸 Demo Walkthrough

Here's a step-by-step walkthrough of a fixed game session on **Normal difficulty** (1-50 range, 8 attempts):

1. **Game starts:** Secret number is generated (let's say 29). Player sees "Range: 1 to 50" and "Attempts left: 7".

2. **First guess - Too High:** Player guesses 40. Game correctly responds "📉 Go LOWER!" (because 40 > 29). Score increases by 5 points. Attempts left: 6.

3. **Second guess - Still Too High:** Player guesses 35. Game responds "📉 Go LOWER!" (because 35 > 29). Score updates. Attempts left: 5.

4. **Third guess - Too Low:** Player guesses 20. Game correctly responds "📈 Go HIGHER!" (because 20 < 29). Score adjusts. Attempts left: 4.

5. **Fourth guess - Correct!:** Player guesses 29. Game displays "🎉 Correct!" with balloons animation. Final score is calculated: 100 - (10 × 5) = 50 points.

6. **New Game Reset:** Player clicks "New Game 🔁". Score properly resets to 0, guess history clears, new secret is generated, and game is ready to play again.

7. **Difficulty Test:** Player switches to "Hard" difficulty. Game now shows "Range: 1 to 100" (previously broken: showed 1-50) and "Attempts allowed: 5" (fewest attempts but largest range = truly harder!).

**Key Behavioral Proof:**
- ✅ Hints now point in correct direction (no more backwards guidance)
- ✅ Easy < Normal < Hard in terms of difficulty (larger ranges, fewer attempts)
- ✅ Game state properly resets between games
- ✅ Score persists correctly during a game, resets on "New Game"

## 🧪 Test Results

```
============================= test session starts =============================
platform win32 -- Python 3.13.7, pytest-9.1.0, pluggy-1.6.0
collected 14 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  7%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 14%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 21%]
tests/test_game_logic.py::test_bug1_too_high_hint_message PASSED         [ 28%]
tests/test_game_logic.py::test_bug1_too_low_hint_message PASSED          [ 35%]
tests/test_game_logic.py::test_bug1_multiple_cases PASSED                [ 42%]
tests/test_game_logic.py::test_bug3_easy_difficulty_range PASSED         [ 50%]
tests/test_game_logic.py::test_bug3_normal_difficulty_range PASSED       [ 57%]
tests/test_game_logic.py::test_bug3_hard_difficulty_range PASSED         [ 64%]
tests/test_game_logic.py::test_bug3_difficulty_progression PASSED        [ 71%]
tests/test_game_logic.py::test_parse_guess_valid_input PASSED            [ 78%]
tests/test_game_logic.py::test_parse_guess_float_input PASSED            [ 85%]
tests/test_game_logic.py::test_parse_guess_invalid_input PASSED          [ 92%]
tests/test_game_logic.py::test_parse_guess_empty_input PASSED            [100%]

============================= 14 passed in 0.13s ==============================
```

**Test Coverage:** All 14 tests pass! This includes:
- 3 foundational tests (winning guess, too high, too low)
- 3 bug-specific tests for backwards hints validation
- 4 difficulty range progression tests  
- 4 helper function tests (parse_guess validation)

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
