import unittest

from challenges import get_challenge, get_next_channel, verify_solution


class TestChallenges(unittest.TestCase):
    def test_welcome_challenge(self):
        """Test the welcome challenge solution."""
        self.assertTrue(verify_solution("#challenge-1-welcome", "fire"))
        self.assertFalse(verify_solution("#challenge-1-welcome", "wrong"))

    def test_binary_challenge(self):
        """Test the binary challenge solution."""
        self.assertTrue(verify_solution("#challenge-2-binary", "paris"))
        self.assertFalse(verify_solution("#challenge-2-binary", "wrong"))

    def test_crypto_challenge(self):
        """Test the crypto challenge solution."""
        self.assertTrue(
            verify_solution("#challenge-3-crypto", "What is the most secret point in the dlrow?")
        )
        self.assertFalse(verify_solution("#challenge-3-crypto", "wrong"))

    def test_challenge_progression(self):
        """Test challenge progression."""
        self.assertEqual(get_next_channel("#challenge-1-welcome"), "#challenge-2-binary")
        self.assertEqual(get_next_channel("#challenge-2-binary"), "#challenge-3-crypto")
        self.assertEqual(get_next_channel("#challenge-3-crypto"), "#challenge-4-timed")
        self.assertEqual(get_next_channel("#challenge-4-timed"), "#challenge-5-vigenere")
        self.assertEqual(get_next_channel("#challenge-5-vigenere"), "#challenge-6-stego")
        self.assertEqual(get_next_channel("#challenge-6-stego"), "#challenge-7-final")
        self.assertIsNone(get_next_channel("#challenge-7-final"))

    def test_challenge_content(self):
        """Test challenge content retrieval."""
        challenge, solution, hint = get_challenge("#challenge-1-welcome")
        self.assertIsNotNone(challenge)
        self.assertIsNotNone(solution)
        self.assertIsNotNone(hint)


if __name__ == "__main__":
    unittest.main()
