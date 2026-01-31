import io
import json

import csv2json


def test_infer_numbers():
    assert csv2json.infer("42") == 42
    assert csv2json.infer("-7") == -7
    assert csv2json.infer("3.5") == 3.5
    assert csv2json.infer("abc") == "abc"

def test_infer_booleans_and_empty():
    assert csv2json.infer("true") is True
    assert csv2json.infer("FALSE") is False
    assert csv2json.infer("") is None
    assert csv2json.infer("null") is None
