from backend.game.logic import evaluate_guess


def test_evaluate_guess_marks_exact_matches():
    assert evaluate_guess("APPLE", "APPLE") == ["GREEN"] * 5


def test_evaluate_guess_marks_wrong_positions():
    assert evaluate_guess("APPLE", "PLEAP") == ["ORANGE"] * 5


def test_evaluate_guess_marks_missing_letters():
    assert evaluate_guess("APPLE", "BRICK") == ["GREY"] * 5


def test_evaluate_guess_combines_all_feedback_types():
    assert evaluate_guess("APPLE", "ALLEY") == [
        "GREEN",
        "ORANGE",
        "GREY",
        "ORANGE",
        "GREY",
    ]


def test_evaluate_guess_does_not_reuse_duplicate_target_letters():
    assert evaluate_guess("APPLE", "LLAMA") == [
        "ORANGE",
        "GREY",
        "ORANGE",
        "GREY",
        "GREY",
    ]