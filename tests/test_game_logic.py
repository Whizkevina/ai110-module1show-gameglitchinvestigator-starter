from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# ========== BUG FIX #1: Backwards Hints Tests ==========
def test_bug1_too_high_hint_message():
    """
    BUG FIX #1: Verify that when guess > secret (too high), 
    the message says "Go LOWER!" not "Go HIGHER!"
    """
    outcome, message = check_guess(60, 42)
    assert outcome == "Too High"
    assert "Go LOWER!" in message, f"Expected 'Go LOWER!' but got: {message}"
    assert "Go HIGHER!" not in message, f"Message should not say 'Go HIGHER!'"


def test_bug1_too_low_hint_message():
    """
    BUG FIX #1: Verify that when guess < secret (too low),
    the message says "Go HIGHER!" not "Go LOWER!"
    """
    outcome, message = check_guess(25, 42)
    assert outcome == "Too Low"
    assert "Go HIGHER!" in message, f"Expected 'Go HIGHER!' but got: {message}"
    assert "Go LOWER!" not in message, f"Message should not say 'Go LOWER!'"


def test_bug1_multiple_cases():
    """
    BUG FIX #1: Test multiple cases to ensure hints are always correct
    """
    test_cases = [
        (75, 50, "Too High", "Go LOWER!"),
        (25, 50, "Too Low", "Go HIGHER!"),
        (100, 1, "Too High", "Go LOWER!"),
        (1, 100, "Too Low", "Go HIGHER!"),
    ]
    
    for guess, secret, expected_outcome, expected_hint in test_cases:
        outcome, message = check_guess(guess, secret)
        assert outcome == expected_outcome, f"Failed for guess={guess}, secret={secret}"
        assert expected_hint in message, f"Expected '{expected_hint}' in message for guess={guess}, secret={secret}, got: {message}"


# ========== BUG FIX #3: Difficulty Configuration Tests ==========
def test_bug3_easy_difficulty_range():
    """
    BUG FIX #3: Verify Easy difficulty has correct range
    """
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20
    

def test_bug3_normal_difficulty_range():
    """
    BUG FIX #3: Verify Normal difficulty has correct range
    """
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 50


def test_bug3_hard_difficulty_range():
    """
    BUG FIX #3: Verify Hard difficulty has LARGEST range (1-100)
    This was the bug: Hard had 1-50, which is smaller than Normal's 1-100
    """
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 100, f"Hard difficulty should have range 1-100, but got 1-{high}"


def test_bug3_difficulty_progression():
    """
    BUG FIX #3: Verify that difficulty ranges progress correctly:
    Easy < Normal < Hard
    """
    easy_range = get_range_for_difficulty("Easy")[1]
    normal_range = get_range_for_difficulty("Normal")[1]
    hard_range = get_range_for_difficulty("Hard")[1]
    
    assert easy_range < normal_range, f"Easy range should be smaller than Normal: {easy_range} vs {normal_range}"
    assert normal_range < hard_range, f"Normal range should be smaller than Hard: {normal_range} vs {hard_range}"


# ========== Helper Function Tests ==========
def test_parse_guess_valid_input():
    """Test that parse_guess correctly parses valid numeric input"""
    ok, guess, error = parse_guess("42")
    assert ok is True
    assert guess == 42
    assert error is None


def test_parse_guess_float_input():
    """Test that parse_guess converts floats to integers"""
    ok, guess, error = parse_guess("42.7")
    assert ok is True
    assert guess == 42
    assert error is None


def test_parse_guess_invalid_input():
    """Test that parse_guess rejects non-numeric input"""
    ok, guess, error = parse_guess("not_a_number")
    assert ok is False
    assert guess is None
    assert error is not None


def test_parse_guess_empty_input():
    """Test that parse_guess rejects empty input"""
    ok, guess, error = parse_guess("")
    assert ok is False
    assert guess is None
    assert error == "Enter a guess."


# ========== CHALLENGE 1: Advanced Edge-Case Testing ==========

def test_edge_case_negative_number():
    """
    Edge Case #1: Negative numbers
    The game logic should handle negative guesses gracefully.
    Since the game ranges are 1-100 (positive), a negative guess should still
    parse correctly but compare correctly to the secret.
    """
    ok, guess, error = parse_guess("-42")
    assert ok is True
    assert guess == -42, "Should parse negative numbers correctly"
    
    # When comparing negative guess to positive secret, should work correctly
    outcome, message = check_guess(-10, 50)
    assert outcome == "Too Low", "Negative guess should correctly be 'Too Low' vs positive secret"
    assert "Go HIGHER!" in message


def test_edge_case_very_large_number():
    """
    Edge Case #2: Very large numbers
    The game should handle extremely large numbers without overflow or errors.
    Comparison should still work correctly.
    """
    ok, guess, error = parse_guess("999999999")
    assert ok is True
    assert guess == 999999999, "Should parse very large numbers"
    
    # Large number should correctly compare
    outcome, message = check_guess(999999999, 50)
    assert outcome == "Too High", "Very large guess should be 'Too High'"
    assert "Go LOWER!" in message


def test_edge_case_float_with_negative():
    """
    Edge Case #3: Negative floats
    The game should handle negative floats that convert to negative integers.
    """
    ok, guess, error = parse_guess("-42.9")
    assert ok is True
    assert guess == -42, "Should convert negative float to negative int"


def test_edge_case_scientific_notation():
    """
    Edge Case #4: Scientific notation
    "1e2" is not a valid game input because it lacks a decimal point,
    so parse_guess tries int() directly which rejects it.
    This is acceptable - the game should not accept scientific notation
    from casual players.
    """
    ok, guess, error = parse_guess("1e2")
    assert ok is False, "Scientific notation without decimal should be rejected"
    assert error == "That is not a number."


def test_edge_case_float_near_integer():
    """
    Edge Case #5: Floats very close to integer boundaries
    Should truncate correctly without rounding errors.
    """
    ok, guess, error = parse_guess("42.9999")
    assert ok is True
    assert guess == 42, "Should truncate 42.9999 to 42, not round to 43"
    
    ok, guess, error = parse_guess("42.0001")
    assert ok is True
    assert guess == 42, "Should truncate 42.0001 to 42"


def test_edge_case_whitespace_input():
    """
    Edge Case #6: Input with whitespace
    Python's int() and float() handle leading/trailing whitespace naturally,
    but we verify this works.
    """
    ok, guess, error = parse_guess("  42  ")
    assert ok is True
    assert guess == 42, "Should parse input with whitespace"


def test_edge_case_zero_guess():
    """
    Edge Case #7: Zero as a guess
    Zero is technically a valid integer, and should compare correctly
    even though it's outside the normal game range.
    """
    ok, guess, error = parse_guess("0")
    assert ok is True
    assert guess == 0, "Should parse zero"
    
    # Zero should compare correctly
    outcome, message = check_guess(0, 50)
    assert outcome == "Too Low", "Zero guess should be 'Too Low' vs 50"
    assert "Go HIGHER!" in message


def test_edge_case_boundary_one():
    """
    Edge Case #8: Guess of 1 (lower boundary of normal game range)
    """
    ok, guess, error = parse_guess("1")
    assert ok is True
    assert guess == 1
    
    # Should compare correctly at boundary
    outcome, message = check_guess(1, 50)
    assert outcome == "Too Low"


def test_edge_case_boundary_hundred():
    """
    Edge Case #9: Guess of 100 (upper boundary of hard difficulty)
    """
    ok, guess, error = parse_guess("100")
    assert ok is True
    assert guess == 100
    
    # Should compare correctly at boundary
    outcome, message = check_guess(100, 50)
    assert outcome == "Too High"


def test_edge_case_guess_equals_secret_edge():
    """
    Edge Case #10: Edge case win at boundary conditions
    Verify win condition works at boundaries.
    """
    outcome, message = check_guess(1, 1)
    assert outcome == "Win", "Should win when guess=1 and secret=1"
    
    outcome, message = check_guess(100, 100)
    assert outcome == "Win", "Should win when guess=100 and secret=100"


def test_edge_case_string_with_plus_sign():
    """
    Edge Case #11: String with explicit plus sign
    "+42" should parse the same as "42"
    """
    ok, guess, error = parse_guess("+42")
    assert ok is True
    assert guess == 42, "Should parse +42 as 42"


def test_edge_case_multiple_decimal_points():
    """
    Edge Case #12: Multiple decimal points should fail gracefully
    "42.5.3" should not parse as it's invalid float format
    """
    ok, guess, error = parse_guess("42.5.3")
    assert ok is False, "Should reject multiple decimal points"
    assert error == "That is not a number."


def test_edge_case_infinity_string():
    """
    Edge Case #13: Infinity strings like "inf"
    Python's float() can parse "inf", but int(float("inf")) raises ValueError
    The game should handle this gracefully
    """
    ok, guess, error = parse_guess("inf")
    assert ok is False, "Should reject 'inf' as invalid game input"
    assert error == "That is not a number."


def test_edge_case_nan_string():
    """
    Edge Case #14: NaN string
    float("nan") is valid Python but int(float("nan")) raises ValueError
    """
    ok, guess, error = parse_guess("nan")
    assert ok is False, "Should reject 'nan' as invalid game input"
    assert error == "That is not a number."
