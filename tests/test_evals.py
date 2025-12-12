# Простейшие unit-тесты для eval-функций
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evals.eval_correctness import check_expected_in_response
from evals.eval_tone_safety import check_politeness, check_hallucination

def test_expected():
    assert check_expected_in_response("Please reset password using https://example.edu/reset", ["reset password"]) == True

def test_politeness_and_hallucination():
    polite = check_politeness("Пожалуйста, помогите мне")
    assert polite is True
    assert check_hallucination("I have reset your password") is False
