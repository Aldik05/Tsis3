# Unit test for response parser (eval_correctness.parse_response_obj)
import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # добавить корень проекта в путь
from evals.eval_correctness import parse_response_obj

def test_parse_string():
    assert parse_response_obj("hello") == "hello"

def test_parse_dict_text():
    assert parse_response_obj({"text":" hi "}) == "hi"

def test_parse_outputs():
    assert parse_response_obj({"outputs":[{"content":" out"}]}) == "out"
