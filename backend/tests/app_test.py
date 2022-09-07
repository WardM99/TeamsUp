"""Basic tests"""
from src.app.app import return_one

def a_test():
    """basic test"""
    assert return_one() == 1
