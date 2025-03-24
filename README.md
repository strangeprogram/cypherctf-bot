# CypherCTF Bot

An advanced IRC-based Capture The Flag (CTF) game bot that creates an engaging and secure challenge environment.

## Features

- 🔒 Secure challenge submission system
- 🎯 Progressive difficulty challenges
- ⏰ Time-based challenges
- 🔐 Cryptographic puzzles
- 📝 Steganography challenges
- 🤖 Automated challenge progression
- 🔑 Private message verification
- 🎮 Interactive command system

## Challenges

1. **Welcome Challenge**
   - Simple riddle to get started
   - Tests basic problem-solving skills

2. **Binary Decoding**
   - Binary to ASCII conversion
   - Pattern recognition

3. **Cryptographic Challenge**
   - Base64 encoding/decoding
   - String manipulation

4. **Time-Based Challenge**
   - Special time-based puzzle
   - Requires timing and patience

5. **Vigenère Cipher**
   - Classical encryption
   - Pattern analysis

6. **Steganography Challenge**
   - Hidden messages in text
   - Pattern recognition

7. **Final Challenge**
   - Multi-step cryptographic puzzle
   - Ultimate test of all skills

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cypherctf-bot.git
cd cypherctf-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your configuration:
```env
BOT_NICK=CTFGameBot
BOT_USERNAME=CTFGameBot
BOT_REALNAME=IRC CTF Game Bot
BOT_PASSWORD=your_secure_password_here
BOT_EMAIL=your_email@example.com
```

4. Run the bot:
```bash
python bot.py
```

## Configuration

The bot can be configured through environment variables or directly in the code:

- `BOT_NICK`: Bot's nickname
- `BOT_USERNAME`: Bot's username
- `BOT_REALNAME`: Bot's real name
- `BOT_PASSWORD`: Password for NickServ registration
- `BOT_EMAIL`: Email for NickServ registration

## Usage

1. Connect to the IRC server
2. Join the main channel (#CypherCon)
3. Type `!start` to begin
4. Follow the challenges in sequence
5. Submit solutions via private message
6. Complete all challenges to win

## Commands

- `!start` - Begin the CTF game
- `!help` - Show help information

## Security Features

- Private message verification
- Channel kick after solving
- Hidden solutions
- Time-based challenges
- Multiple verification methods

## Development

To add new challenges:

1. Edit `challenges.py`
2. Add your challenge to the `CHALLENGES` dictionary
3. Include challenge text, solution, and hints
4. Test thoroughly before deployment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

ISC License

Copyright (c) 2025, strangeprogram blowfish@hivemind 