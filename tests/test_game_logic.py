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
