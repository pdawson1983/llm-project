def test_modulus():
    assert 10 % 3 == 1
    assert 15 % 5 == 0
    assert 7 % 2 == 1

def run_tests():
    test_modulus()
    print("All tests passed!")

run_tests()