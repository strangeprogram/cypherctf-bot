import unittest
from unittest.mock import MagicMock, patch
from bot import CTFGame
from challenges import CHALLENGES, verify_solution, get_next_channel

class TestCTFGame(unittest.TestCase):
    def setUp(self):
        self.mock_bot = MagicMock()
        self.mock_bot.nick = "CTFGameBot"
        self.mock_bot.log = MagicMock()
        self.mock_bot.config = {}
        self.game = CTFGame(self.mock_bot)

    def test_challenge_verification(self):
        """Test that challenge solutions are correctly verified"""
        # Test correct solutions
        self.assertTrue(verify_solution("#challenge-1-welcome", "fire"))
        self.assertTrue(verify_solution("#challenge-2-binary", "paris"))
        self.assertTrue(verify_solution("#challenge-3-crypto", "the most secret point in the world is the one that's never spoke"))
        self.assertTrue(verify_solution("#challenge-4-final", "CTF{1RC_Ch4ll3ng3_M4st3r}"))

        # Test incorrect solutions
        self.assertFalse(verify_solution("#challenge-1-welcome", "water"))
        self.assertFalse(verify_solution("#challenge-2-binary", "london"))
        self.assertFalse(verify_solution("#challenge-3-crypto", "wrong answer"))
        self.assertFalse(verify_solution("#challenge-4-final", "wrong flag"))

    def test_next_channel(self):
        """Test that next channels are correctly determined"""
        self.assertEqual(get_next_channel("#challenge-1-welcome"), "#challenge-2-binary")
        self.assertEqual(get_next_channel("#challenge-2-binary"), "#challenge-3-crypto")
        self.assertEqual(get_next_channel("#challenge-3-crypto"), "#challenge-4-final")
        self.assertEqual(get_next_channel("#challenge-4-final"), "")

    def test_challenge_content(self):
        """Test that challenge content is properly formatted"""
        for channel, (challenge, solution, next_channel) in CHALLENGES.items():
            self.assertIsInstance(challenge, str)
            self.assertIsInstance(solution, str)
            self.assertIsInstance(next_channel, (str, type(None)))
            self.assertTrue(len(challenge) > 0)
            self.assertTrue(len(solution) > 0)

    def test_handle_join(self):
        """Test the join handler"""
        mock_mask = MagicMock()
        mock_mask.nick = "TestUser"
        
        # Test joining a challenge channel
        self.game.handle_join(mock_mask, "#challenge-1-welcome")
        self.mock_bot.privmsg.assert_called_once()

    def test_handle_challenge_solution(self):
        """Test challenge solution handling"""
        mock_mask = MagicMock()
        mock_mask.nick = "TestUser"

        # Test correct solution
        self.game.handle_challenge_solution(mock_mask, "fire")
        self.mock_bot.privmsg.assert_called_with(
            mock_mask.nick,
            "Correct! Join #challenge-2-binary for the next challenge!"
        )

        # Test final challenge solution
        self.mock_bot.privmsg.reset_mock()
        self.game.handle_challenge_solution(mock_mask, "CTF{1RC_Ch4ll3ng3_M4st3r}")
        self.mock_bot.privmsg.assert_called_with(
            mock_mask.nick,
            "Congratulations! You've completed all challenges!"
        )

if __name__ == '__main__':
    unittest.main() 