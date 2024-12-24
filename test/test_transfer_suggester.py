import pytest
from src.transfer_suggester import transfer_suggester

# no return value
# prints to console
# items printed to console have correct keys
# items printed have correct values

def test_transfer_suggester_has_no_return():
    assert transfer_suggester() == None