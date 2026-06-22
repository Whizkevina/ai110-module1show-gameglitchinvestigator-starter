# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game on Normal difficulty, I immediately noticed something was wrong. The game appeared to run, but after making several guesses, the hints were telling me the opposite direction from what made sense. For example, when I guessed 50 and the secret was 42, the hint said "Go HIGHER!" but my guess was already too high. Additionally, when I changed to Hard difficulty, it had a much smaller number range (1-50 vs 1-100 on Normal) and fewer attempts (5 vs 8), making it actually easier, not harder. Finally, when I clicked "New Game," the score and guess history persisted from the previous game instead of resetting.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| 50 (secret: 42) | Hint: "Go LOWER!" (too high) | Hint: "Go HIGHER!" (backwards) | none |
| 25 (secret: 42) | Hint: "Go HIGHER!" (too low) | Hint: "Go LOWER!" (backwards) | none |
| 75 (secret: 42) | Hint: "Go LOWER!" (too high) | Hint: "Go HIGHER!" (backwards) | none |
| Click "New Game" on Normal | Score resets to 0, history clears | Score stays at -5, history shows [50, 75, 25] | none |
| Switch to Hard difficulty | Range should be larger/harder | Range is 1-50 (smaller), 5 attempts (fewer) | none |

**Detailed Analysis of Bugs Found:**

1. **Backwards Hints** (in `check_guess()` function):
   - When guess > secret (too high), the function returns message "📈 Go HIGHER!" but should say "📉 Go LOWER!"
   - When guess < secret (too low), the function returns message "📉 Go LOWER!" but should say "📈 Go HIGHER!"
   - The emoji directions also don't match - should be opposite

2. **Game State Not Fully Reset** (in New Game button handler):
   - `st.session_state.score` is not reset to 0 - carries over from previous game
   - `st.session_state.history` is not cleared - shows all previous guesses
   - `st.session_state.secret` uses hardcoded range (1, 100) instead of current difficulty range

3. **Difficulty Configuration Reversed** (in `get_range_for_difficulty()` function):
   - Hard mode: 1-50 range with 5 attempts (should be harder!)
   - Normal mode: 1-100 range with 8 attempts  
   - Easy mode: 1-20 range with 6 attempts
   - Hard should have a LARGER range and FEWER attempts to be more challenging, but it's the opposite!

4. **Bonus Bug - Alternating Int/String Comparison** (around line 157 in app.py):
   - On even attempts, code converts secret to string: `secret = str(st.session_state.secret)`
   - This causes string comparison instead of numeric comparison
   - String "100" < "42" (lexicographic), but numeric 100 > 42
   - Leads to incorrect "Too High"/"Too Low" outcomes on alternating attempts

---

## 2. How did you use AI as a teammate?

I used GitHub Copilot (Claude-based AI) to help identify and fix the bugs. **Correct AI suggestion:** When I asked Copilot to refactor the `check_guess()` function into `logic_utils.py` and fix the backwards hints, it correctly swapped the messages - changing "Go HIGHER!" to "Go LOWER!" when guess > secret, and vice versa. I verified this was correct by: (1) running the pytest tests which all passed, and (2) playing the game manually: guessing 40 against secret 29 now correctly showed "Go LOWER!" instead of the previous "Go HIGHER!". **Misleading AI suggestion:** The AI initially suggested only changing the hint messages without considering the full logic refactor. When I prompted for a more complete solution that included refactoring all game logic functions into logic_utils.py and fixing the difficulty ranges in one go, the AI was then able to provide a more comprehensive and correct solution. This taught me to give detailed, multi-step instructions to AI rather than piecemeal requests.

---

## 3. Debugging and testing your fixes

I used a three-layer testing approach: (1) **Unit tests with pytest** - Created 14 comprehensive tests including specific bug-fix tests like `test_bug1_too_high_hint_message()` that verifies when guess > secret, the message contains "Go LOWER!". All 14 tests pass. (2) **Manual game testing** - Played the game and made specific guesses to verify the hints were correct. For example, with secret=29, guessing 40 correctly showed "📉 Go LOWER!" instead of "📈 Go HIGHER!". (3) **Difficulty verification** - Switched between difficulty levels and confirmed Hard now shows range 1-100 (vs the buggy 1-50), while Normal shows 1-50. The pytest test `test_bug3_difficulty_progression()` specifically verifies that Easy < Normal < Hard in terms of range size. The fixes are definitely working - the game now provides correct feedback!

---

## 4. What did you learn about Streamlit and state?

Streamlit "reruns" are when the entire script re-executes from top to bottom whenever a user interacts with a widget. Session state is a dictionary (`st.session_state`) that persists values across reruns, allowing you to keep track of game progress like the secret number, attempt count, and score. Without session state, variables would reset on every rerun. In this game, when you click "Submit Guess," Streamlit reruns the entire app.py script, but because we saved the secret in `st.session_state.secret`, it remembers the current secret instead of generating a new one. The bug with the "New Game" button not clearing history was because we didn't explicitly reset all session state variables - we only reset `attempts` and `secret`, but forgot to reset `score` and `history`.

---

## 5. Looking ahead: your developer habits

One habit I want to reuse is **creating comprehensive tests alongside fixes**. Before I fixed the bugs, I created 14 specific pytest tests that directly targeted each bug. This made me confident the fixes were working and prevented regression. I will apply this to future projects - write tests that fail for the buggy code, then watch them pass after fixes. **One thing I would do differently:** Next time working with AI on code fixes, I'd ask the AI to generate the test cases FIRST (test-driven development style), then implement the fixes to make the tests pass. This ensures the AI and I agree on what "correct" looks like before writing any fix code. This project taught me that **AI-generated code needs rigorous testing** - not because AI is unreliable, but because without tests, it's too easy to miss subtle issues. The backwards hints were a simple logic error, but finding and fixing it required both automated tests AND manual testing to be truly confident.
