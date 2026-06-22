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

## ✨ Enhanced UI Features

The game has been upgraded with modern, professional styling and improved user experience:

### Visual Improvements:
- **Gradient Title** - Beautiful purple/blue gradient for the main title creating visual impact
- **Difficulty Badges** - Color-coded difficulty indicators (🎯 Normal, 🔥 Hard, 😊 Easy) for quick reference
- **Progress Tracking** - Visual progress bar showing attempts used vs. available  
- **Score Display** - Star-emoji highlighted score box with premium styling
- **Game Stats Sidebar** - Metrics showing Range (🎲) and Attempts (❤️) with professional layout
- **Enhanced Info Box** - Better formatted game instructions with emoji icons and semantic colors
- **Improved Button Layout** - Full-width responsive buttons with better spacing
- **Professional Footer** - Enhanced footer showcasing project stats and documentation

### CSS Enhancements:
- Custom gradient backgrounds for key elements
- Color-coded visual hierarchy (purple for info, green for easy, yellow for normal, red for hard)
- Smooth borders and rounded corners for modern aesthetics
- Icon integration throughout the interface for visual clarity
- Responsive layout that adapts to different screen sizes

### Current UI Screenshot:
The enhanced game features a modern, professional interface with:
- **Main Title**: Eye-catching gradient text with game controller emoji
- **Settings Panel**: Clean sidebar with difficulty selector and game stats  
- **Progress Indicators**: Visual progress bar and attempt counter
- **Score Display**: Prominent star-decorated score box
- **Info Section**: Color-coded game instructions with emoji guides
- **Input Area**: Intuitive text input with helpful placeholder text
- **Action Buttons**: Full-width responsive buttons (Submit, New Game, Show Hint)
- **Professional Footer**: Project documentation and achievements

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
collected 28 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  3%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [  7%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 10%]
tests/test_game_logic.py::test_bug1_too_high_hint_message PASSED         [ 14%]
tests/test_game_logic.py::test_bug1_too_low_hint_message PASSED          [ 17%]
tests/test_game_logic.py::test_bug1_multiple_cases PASSED                [ 21%]
tests/test_game_logic.py::test_bug3_easy_difficulty_range PASSED         [ 25%]
tests/test_game_logic.py::test_bug3_normal_difficulty_range PASSED       [ 28%]
tests/test_game_logic.py::test_bug3_hard_difficulty_range PASSED         [ 32%]
tests/test_game_logic.py::test_bug3_difficulty_progression PASSED        [ 35%]
tests/test_game_logic.py::test_parse_guess_valid_input PASSED            [ 39%]
tests/test_game_logic.py::test_parse_guess_float_input PASSED            [ 42%]
tests/test_game_logic.py::test_parse_guess_invalid_input PASSED          [ 46%]
tests/test_game_logic.py::test_parse_guess_empty_input PASSED            [ 50%]
tests/test_game_logic.py::test_edge_case_negative_number PASSED          [ 53%]
tests/test_game_logic.py::test_edge_case_very_large_number PASSED        [ 57%]
tests/test_game_logic.py::test_edge_case_float_with_negative PASSED      [ 60%]
tests/test_game_logic.py::test_edge_case_scientific_notation PASSED      [ 64%]
tests/test_game_logic.py::test_edge_case_float_near_integer PASSED       [ 67%]
tests/test_game_logic.py::test_edge_case_whitespace_input PASSED         [ 71%]
tests/test_game_logic.py::test_edge_case_zero_guess PASSED               [ 75%]
tests/test_game_logic.py::test_edge_case_boundary_one PASSED             [ 78%]
tests/test_game_logic.py::test_edge_case_boundary_hundred PASSED         [ 82%]
tests/test_game_logic.py::test_edge_case_guess_equals_secret_edge PASSED [ 85%]
tests/test_game_logic.py::test_edge_case_string_with_plus_sign PASSED    [ 89%]
tests/test_game_logic.py::test_edge_case_multiple_decimal_points PASSED  [ 92%]
tests/test_game_logic.py::test_edge_case_infinity_string PASSED          [ 96%]
tests/test_game_logic.py::test_edge_case_nan_string PASSED               [100%]

============================= 28 passed in 0.21s ==============================
```

**Test Coverage:** All 28 tests pass! This includes:
- 3 foundational tests (winning guess, too high, too low)
- 3 bug-specific tests for backwards hints validation
- 4 difficulty range progression tests  
- 4 helper function tests (parse_guess validation)
- **14 advanced edge-case tests (CHALLENGE 1)** including:
  - Negative numbers and very large numbers
  - Float-to-int conversion edge cases
  - Boundary conditions (0, 1, 100)
  - Whitespace handling
  - Invalid inputs (infinity, NaN, multiple decimals)

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
