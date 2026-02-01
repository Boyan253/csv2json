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


def test_convert_reads_rows(tmp_path):
    p = tmp_path / "in.csv"
    p.write_text("name,age\nada,36\ngrace,45\n", encoding="utf-8")
    rows = list(csv2json.convert(str(p), do_infer=True))
    assert rows == [{"name": "ada", "age": 36}, {"name": "grace", "age": 45}]

def test_convert_without_infer_keeps_strings(tmp_path):
    p = tmp_path / "in.csv"
    p.write_text("n\n1\n", encoding="utf-8")
    assert list(csv2json.convert(str(p))) == [{"n": "1"}]
