"""Basic tests"""
from src.app.app import return_one

def test_return_one():
    """basic test"""
    assert return_one() == 1
