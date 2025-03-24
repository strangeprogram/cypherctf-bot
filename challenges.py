import base64
import hashlib
import random
import re
import string
import time
from datetime import datetime


def generate_vigenere_key():
    """Generate a random Vigenère cipher key."""
    return "".join(random.choices(string.ascii_lowercase, k=8))


def vigenere_encrypt(text, key):
    """Encrypt text using Vigenère cipher."""
    result = []
    key = key.lower()
    key_length = len(key)
    for i, char in enumerate(text.lower()):
        if char.isalpha():
            # Convert to 0-25 range
            text_num = ord(char) - ord("a")
            key_num = ord(key[i % key_length]) - ord("a")
            # Apply Vigenère cipher
            result_num = (text_num + key_num) % 26
            result.append(chr(result_num + ord("a")))
        else:
            result.append(char)
    return "".join(result)


def create_steganography_text():
    """Create a text with hidden message using steganography."""
    # The hidden message is "hidden message"
    # We'll use the first letter of each word to spell it out
    text = (
        "Hello everyone, welcome to this challenge.\n"
        "I hope you're enjoying the game so far.\n"
        "Don't forget to check every detail carefully.\n"
        "Each word might hold a secret, you never know.\n"
        "Nobody said this would be easy, but it's fun!\n"
        "Maybe you'll find something interesting here.\n"
        "Always look for patterns in the text.\n"
        "Some secrets are hidden in plain sight.\n"
        "See if you can spot what's different.\n"
        "Good luck finding the hidden message!\n"
        "Everyone has their own way of solving puzzles."
    )
    return text


def generate_challenges():
    """Generate dynamic challenges with random elements."""
    # Generate a random Vigenère key
    vigenere_key = generate_vigenere_key()

    return {
        "#challenge-1-welcome": {
            "challenge": (
                "🎯 Welcome to the IRC CTF Challenge!\n"
                "🔍 Your first challenge is a simple one:\n"
                "What is the opposite of water?\n"
                "💡 By your powers combined I am Captain Planet!"
            ),
            "solution": "fire",
            "hint": "By your powers combined I am Captain Planet!",
        },
        "#challenge-2-binary": {
            "challenge": (
                "🎯 Decoding Challenge\n"
                "🔍 Decode:\n"
                "01110000 01100001 01110010 01101001 01110011\n"
                "💡 The city of lights holds many secrets...\n"
            ),
            "solution": "paris",
            "hint": "The city of lights holds many secrets...",
        },
        "#challenge-3-crypto": {
            "challenge": (
                "🎯 Cryptographic Challenge\n"
                "🔍 Decode this message:\n"
                "V2hhdCBpcyB0aGUgbW9zdCBzZWNyZXQgcG9pbnQgaW4gdGhlIHdvcmxkPw==\n"
                "💡 Sometimes the spoken point is hidden in plain thgis....\n"
            ),
            "solution": "What is the most secret point in the dlrow?",
            "hint": "Sometimes the truth is hidden in plain thgis....",
        },
        "#challenge-4-timed": {
            "challenge": (
                "⏰ Time-Based Challenge\n"
                "🔍 This challenge can only be solved at a specific time.\n"
                "💡 The time is encoded in this riddle:\n"
                "When the clock strikes 4:20,\n"
                "The answer will be clear to see.\n"
                "🎮 Hint: The answer is a single word related to the time."
            ),
            "solution": "blaze",
            "hint": "The answer lies in the smoke...",
        },
        "#challenge-5-vigenere": {
            "challenge": (
                "🔐 Cipher Challenge\n"
                "🔍 Decrypt this message:\n"
                f"{vigenere_encrypt('the quick brown fox jumps over the lazy dog', vigenere_key)}\n"
                "💡 The key is: {vigenere_key}\n"
            ),
            "solution": "the quick brown fox jumps over the lazy dog",
            "hint": "The key to understanding is in the pattern...",
        },
        "#challenge-6-stego": {
            "challenge": (
                "🔍 Steganography Challenge\n"
                "🔐 There's a hidden message in this text:\n\n"
                f"{create_steganography_text()}\n\n"
                "💡 Look for patterns in the text\n"
            ),
            "solution": "hidden message",
            "hint": "In the beginning their was truth...",
        },
        "#challenge-7-final": {
            "challenge": (
                "🎯 Final Challenge - The Ultimate Puzzle\n"
                "🔍 Solve this puzzle:\n"
                "1. Take the MD5 hash of 'irc_challenge_master'\n"
                "2. Convert it to base64\n"
                "3. Take the first 8 characters\n"
                "4. Add 'ctf{' at the start and '}' at the end\n"
                "5. Replace all 'a' with '4', 'e' with '3', 'i' with '1', 'o' with '0'\n"
            ),
            "solution": "ctf{1rc_ch4ll3ng3_m4st3r}",
            "hint": "💡 The format should be: ctf{...}",
        },
    }


# Initialize challenges
CHALLENGES = generate_challenges()


def get_challenge(channel):
    """Get challenge details for a channel."""
    if channel in CHALLENGES:
        challenge = CHALLENGES[channel]["challenge"]
        solution = CHALLENGES[channel]["solution"]
        hint = CHALLENGES[channel]["hint"]
        return challenge, solution, hint
    return None, None, None


def verify_solution(channel, user_solution):
    """Verify if a user's solution is correct."""
    if channel in CHALLENGES:
        # Check time-based challenge
        if CHALLENGES[channel].get("time_check", False):
            current_time = datetime.now()
            if current_time.hour != 4 or current_time.minute != 20:
                print(
                    f"Time check failed: Current time is {current_time.hour}:{current_time.minute}"
                )
                return False

        expected = CHALLENGES[channel]["solution"].lower()
        actual = user_solution.lower().strip()
        print(f"Verifying solution for {channel}:")
        print(f"Expected: '{expected}'")
        print(f"Actual: '{actual}'")
        print(f"Match: {expected == actual}")
        return expected == actual
    return False


def get_next_channel(current_channel):
    """Get the next challenge channel."""
    channels = list(CHALLENGES.keys())
    try:
        current_index = channels.index(current_channel)
        if current_index < len(channels) - 1:
            return channels[current_index + 1]
    except ValueError:
        pass
    return None


def refresh_challenges():
    """Refresh challenges with new random elements."""
    global CHALLENGES
    CHALLENGES = generate_challenges()
