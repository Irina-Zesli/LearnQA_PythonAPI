class TestPhrase:
    def test_check_phrase(self):
        phrase = input("Set a phrase: ")
        expected_len_less = 15
        assert len(phrase) < expected_len_less, f"Length is not less than {expected_len_less}"