# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Test Generation (SF7) - Challenge 1: Advanced Edge-Case Testing

> Document how you used AI to help generate or improve tests.

**Primary Prompt:**
> "I'm building a number guessing game where users enter guesses. The parse_guess() function converts string input to integers. What are 10-15 edge case inputs that could break or behave unexpectedly? Consider: negative numbers, very large numbers, floats, special values like infinity/NaN, whitespace, boundary conditions, and invalid formats. For each edge case, explain why it's important to test."

**Edge Cases Identified & Tested:**

| Edge Case | Prompt Suggestion | Test Implementation | Pass Status | Why This Matters |
|-----------|------------------|-------------------|------------|-----------------|
| Negative Numbers | Test how negative values compare against positive secret | `test_edge_case_negative_number`: parse "-42", verify correct comparison | ✅ PASS | Game range is 1-100 but comparison logic should work with any int |
| Very Large Numbers | Test for integer overflow or parsing errors | `test_edge_case_very_large_number`: parse "999999999" | ✅ PASS | Python handles arbitrary precision, but good to verify no crashes |
| Negative Floats | Test float + negative combination | `test_edge_case_float_with_negative`: parse "-42.9" → -42 | ✅ PASS | Combines two conversion edge cases into one |
| Scientific Notation | Test unusual but technically numeric format | `test_edge_case_scientific_notation`: reject "1e2" gracefully | ✅ PASS | Should not accept scientific notation from casual game input |
| Float Precision | Test truncation vs rounding behavior | `test_edge_case_float_near_integer`: "42.9999" → 42 not 43 | ✅ PASS | Clarifies truncation is the intended behavior |
| Whitespace | Test real-world input with spaces | `test_edge_case_whitespace_input`: parse "  42  " → 42 | ✅ PASS | Common user input pattern that must be handled |
| Zero | Test lower boundary outside game range | `test_edge_case_zero_guess`: parse "0", verify comparison | ✅ PASS | Edge case for range boundary testing |
| Boundary Conditions (1 & 100) | Test exact game range limits | `test_edge_case_boundary_one` & `test_edge_case_boundary_hundred` | ✅ PASS | Extremes where win conditions occur |
| Winning at Boundaries | Test win condition at range extremes | `test_edge_case_guess_equals_secret_edge`: guess=secret=100 | ✅ PASS | Ensure win logic works at boundaries |
| Plus Sign | Test explicit positive notation | `test_edge_case_string_with_plus_sign`: "+42" → 42 | ✅ PASS | Alternative numeric format that should parse |
| Multiple Decimals | Test malformed float input | `test_edge_case_multiple_decimal_points`: reject "42.5.3" | ✅ PASS | Invalid format should be rejected gracefully |
| Infinity | Test special float value | `test_edge_case_infinity_string`: reject "inf" | ✅ PASS | Mathematical special value should not crash game |
| NaN | Test Not-a-Number value | `test_edge_case_nan_string`: reject "nan" | ✅ PASS | Special value that should be rejected |

**Results:** All 28 tests passing (14 original + 14 new edge cases)
- Execution time: 0.21 seconds
- 100% pass rate
- Robust input validation confirmed across unusual inputs

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
