import asyncio
import irc3
from irc3.plugins.command import command
from irc3.plugins.cron import cron
import os
from dotenv import load_dotenv
from challenges import CHALLENGES, get_challenge, verify_solution, get_next_channel

# Load environment variables
load_dotenv()

@irc3.plugin
class CTFGame:
    def __init__(self, bot):
        self.bot = bot
        self.log = bot.log
        self.config = bot.config
        self.channels = set()
        self.active_challenges = {}
        self.log.info('CTFGame plugin initialized')
        self.registered = False
        self.topic_retries = {}  # Track topic setting retries per channel

    def server_ready(self):
        """Called when the bot is ready to join channels."""
        self.log.info('Server ready! Attempting to join channels...')
        try:
            # Join all channels immediately
            asyncio.create_task(self.join_channels())
            
            # Register with NickServ if not already registered
            if not self.registered:
                self.log.info('Attempting to register with NickServ...')
                self.bot.privmsg('NickServ', f'REGISTER {self.config["password"]} {self.config["email"]}')
        except Exception as e:
            self.log.error(f'Error during registration: {str(e)}')

    @irc3.event(irc3.rfc.PRIVMSG)
    def handle_nickserv(self, mask, event, target, data):
        """Handle NickServ messages."""
        if target == self.bot.nick:
            self.log.info(f'NickServ message: {data}')
            if 'Your nickname is not registered' in data:
                self.log.info('Attempting to register nickname...')
                self.bot.privmsg('NickServ', f'REGISTER {self.config["password"]} {self.config["email"]}')
            elif 'Registration successful' in data:
                self.log.info('Registration successful!')
                self.registered = True
                # Join channels after successful registration
                asyncio.create_task(self.join_channels())
            elif 'Password accepted' in data:
                self.log.info('Password accepted!')
                self.registered = True
                # Join channels after successful authentication
                asyncio.create_task(self.join_channels())

    async def join_channels(self):
        """Join all required channels."""
        try:
            # Join the main channel
            self.log.info('Joining #CypherCon...')
            self.bot.join('#CypherCon')
            
            # Join all challenge channels
            for channel in CHALLENGES.keys():
                self.log.info(f'Joining {channel}...')
                self.bot.join(channel)
                # Add a small delay between joins to avoid flood protection
                await asyncio.sleep(1)
        except Exception as e:
            self.log.error(f'Error joining channels: {str(e)}')

    def set_channel_topic(self, channel, topic):
        """Set channel topic with retry mechanism."""
        if channel not in self.topic_retries:
            self.topic_retries[channel] = 0
        
        if self.topic_retries[channel] < 3:
            try:
                self.log.info(f'Setting topic for {channel} (attempt {self.topic_retries[channel] + 1})')
                self.bot.topic(channel, topic)
                self.topic_retries[channel] += 1
            except Exception as e:
                self.log.error(f'Error setting topic for {channel}: {str(e)}')
                self.topic_retries[channel] += 1
        else:
            self.log.warning(f'Max retries reached for setting topic in {channel}')

    @irc3.event(irc3.rfc.JOIN)
    def handle_join(self, mask, channel, **kwargs):
        """Handle when users join channels."""
        self.log.info(f'Join event: {mask.nick} joined {channel}')
        
        # Set channel topic for challenge channels
        if channel in CHALLENGES:
            challenge, _, _ = get_challenge(channel)
            self.log.info(f'Setting topic for {channel}')
            self.set_channel_topic(channel, f"🎮 CTF Challenge Channel | Solve the challenge to get the next channel!")
            
            # Send welcome message with challenge
            welcome_msg = (
                f"👋 Welcome {mask.nick} to {channel}!\n"
                f"🎯 Here's your challenge:\n"
                f"{challenge}\n"
                f"💡 Submit your answer in the channel or via private message."
            )
            self.log.info(f'Sending challenge to {mask.nick} in {channel}')
            self.bot.privmsg(channel, welcome_msg)
            # Also send privately
            self.bot.privmsg(mask.nick, welcome_msg)
        
        # Set topic for main channel
        elif channel == '#CypherCon':
            self.log.info('Setting topic for main channel')
            self.set_channel_topic(channel, "🎮 IRC CTF Game | Find hidden channels and solve challenges!")
            
            # Send welcome message to main channel
            welcome_msg = (
                f"👋 Welcome {mask.nick} to the IRC CTF Game!\n"
                f"🎯 Find hidden channels and solve challenges to progress.\n"
                f"💡 Type !start to begin your journey!"
            )
            self.bot.privmsg(channel, welcome_msg)
            # Also send privately
            self.bot.privmsg(mask.nick, welcome_msg)

    @irc3.event(irc3.rfc.JOIN)
    def handle_bot_join(self, mask, channel, **kwargs):
        """Handle when the bot joins channels."""
        if mask.nick == self.bot.nick:
            if channel == '#CypherCon':
                self.log.info('Bot joined main channel, sending initial message')
                self.bot.privmsg(channel, (
                    "🎮 Welcome to the IRC CTF Game!\n"
                    "🎯 Your mission is to find hidden channels and solve challenges.\n"
                    "💡 Type !start to begin your journey!\n"
                    "❓ Type !help for more information"
                ))
            # Reset topic retries when bot joins a channel
            self.topic_retries[channel] = 0

    @irc3.event(irc3.rfc.KICK)
    def handle_kick(self, mask, channel, target, reason, **kwargs):
        """Handle when the bot is kicked from a channel."""
        if target == self.bot.nick:
            self.log.info(f'Bot was kicked from {channel} by {mask.nick}: {reason}')
            # Rejoin the channel after a short delay
            asyncio.create_task(self.rejoin_channel(channel))

    @irc3.event(irc3.rfc.PART)
    def handle_part(self, mask, channel, **kwargs):
        """Handle when the bot parts from a channel."""
        if mask.nick == self.bot.nick:
            self.log.info(f'Bot parted from {channel}')
            # Rejoin the channel after a short delay
            asyncio.create_task(self.rejoin_channel(channel))

    async def rejoin_channel(self, channel):
        """Rejoin a channel after a delay."""
        await asyncio.sleep(5)  # Wait 5 seconds before rejoining
        self.log.info(f'Attempting to rejoin {channel}')
        try:
            self.bot.join(channel)
        except Exception as e:
            self.log.error(f'Error rejoining {channel}: {str(e)}')

    def handle_command(self, mask, target, data):
        """Handle bot commands."""
        if data.startswith('!'):
            command = data[1:].lower()
            self.log.info(f'Command received: {command} from {mask.nick}')
            
            if command == 'start':
                # Send to both channel and user
                self.bot.privmsg(target, f"🎯 {mask.nick}, check your private messages for instructions!")
                self.bot.privmsg(mask.nick, (
                    f"🎯 {mask.nick}, your first challenge awaits!\n"
                    f"🔍 Join #challenge-1-welcome to begin.\n"
                    f"💡 Type: /join #challenge-1-welcome"
                ))
            elif command == 'help':
                # Send to both channel and user
                self.bot.privmsg(target, f"❓ {mask.nick}, check your private messages for help!")
                self.bot.privmsg(mask.nick, (
                    f"🎮 IRC CTF Game Help:\n"
                    f"!start - Begin your journey\n"
                    f"!help - Show this help message\n"
                    f"💡 Each challenge will lead you to the next channel\n"
                    f"🎯 Solve all challenges to win!"
                ))

    @irc3.event(irc3.rfc.PRIVMSG)
    def handle_channel_msg(self, mask, event, target, data):
        """Handle channel messages."""
        # Skip if the message is from the bot itself
        if mask.nick == self.bot.nick:
            return
            
        # Only process channel messages
        if target.startswith('#'):
            self.log.info(f'Channel message in {target} from {mask.nick}: {data}')
            
            # Handle commands in the main channel
            if target == '#ctf-game':
                self.handle_command(mask, target, data)
            
            # For challenge solutions in channel, always say incorrect
            elif target in CHALLENGES:
                self.log.info(f'Solution attempt in channel from {mask.nick} in {target}')
                self.bot.privmsg(target, f"❌ {mask.nick}, that's not correct. Try again!")
                # Send private message to guide them
                self.bot.privmsg(mask.nick, (
                    f"💡 Hey {mask.nick}!\n"
                    f"To submit solutions, please send them to me privately.\n"
                    f"This keeps the answers secret for other players.\n"
                    f"Try sending your answer directly to me!"
                ))

    @irc3.event(irc3.rfc.PRIVMSG)
    def handle_privmsg(self, mask, event, target, data):
        """Handle private messages."""
        if target == self.bot.nick:  # Only process direct messages to the bot
            self.log.info(f'Private message from {mask.nick}: {data}')
            # For private messages, we don't know the channel, so pass None
            self.handle_challenge_solution(mask, data, current_channel=None)

    @irc3.event('NOTICE')
    def handle_notice(self, mask, event, target, data):
        """Handle notice messages."""
        if target == self.bot.nick:  # Only process notices to the bot
            self.log.info(f'Notice from {mask.nick}: {data}')
            # Handle notices the same way as private messages
            self.handle_challenge_solution(mask, data, current_channel=None)

    def handle_challenge_solution(self, mask, solution, current_channel=None):
        """Handle challenge solutions."""
        self.log.info(f'Processing solution from {mask.nick}: {solution}')
        
        # For channel messages, only check that specific channel
        if current_channel and current_channel in CHALLENGES:
            self.log.info(f'Checking solution for channel: {current_channel}')
            if verify_solution(current_channel, solution):
                self.log.info(f'Solution verified for {current_channel}!')
                self._send_success_messages(mask, current_channel)
                # Kick user from channel after solving
                self.bot.kick(current_channel, mask.nick, "Challenge solved! Check your private messages for the next challenge.")
                return
        
        # For private messages, check all channels
        elif not current_channel:
            for channel in CHALLENGES.keys():
                self.log.info(f'Checking solution for channel: {channel}')
                if verify_solution(channel, solution):
                    self.log.info(f'Solution verified for {channel}!')
                    self._send_success_messages(mask, channel)
                    # Kick user from channel after solving
                    self.bot.kick(channel, mask.nick, "Challenge solved! Check your private messages for the next challenge.")
                    return

    def _send_success_messages(self, mask, solved_channel):
        """Send success messages to the user."""
        self.log.info(f'Preparing success messages for {mask.nick} in {solved_channel}')
        next_channel = get_next_channel(solved_channel)
        
        if next_channel:
            self.log.info(f'Correct solution! Notifying {mask.nick} about next channel: {next_channel}')
            
            try:
                # Send success message privately
                success_msg = f"🎉 Congratulations! You've solved the challenge in {solved_channel}!"
                self.log.info(f'Sending success message to {mask.nick}')
                self.bot.privmsg(mask.nick, success_msg)
                
                # Get and send next challenge details privately
                next_challenge, _, _ = get_challenge(next_channel)
                next_msg = (
                    f"🎯 Your next challenge awaits in: {next_channel}\n"
                    f"💡 Type this command to join: /join {next_channel}\n"
                    f"\n📝 Here's a preview of your next challenge:\n"
                    f"{next_challenge}"
                )
                self.log.info(f'Sending next challenge details to {mask.nick}')
                self.bot.privmsg(mask.nick, next_msg)
            except Exception as e:
                self.log.error(f'Error sending messages to {mask.nick}: {str(e)}')
                # Try to send a simpler message if the detailed one fails
                try:
                    self.bot.privmsg(mask.nick, f"🎉 Congratulations! Join {next_channel} for your next challenge!")
                except Exception as e2:
                    self.log.error(f'Error sending fallback message: {str(e2)}')
        else:
            self.log.info(f'Final challenge completed by {mask.nick}!')
            try:
                final_msg = (
                    f"🏆 CONGRATULATIONS {mask.nick}! 🏆\n"
                    f"You've completed all challenges in the CTF game!\n"
                    f"Thank you for playing! 🎮"
                )
                self.log.info(f'Sending final congratulations to {mask.nick}')
                self.bot.privmsg(mask.nick, final_msg)
            except Exception as e:
                self.log.error(f'Error sending final message to {mask.nick}: {str(e)}')

def main():
    # Bot configuration
    config = {
        'host': 'irc.supernets.org',
        'port': 6667,
        'nick': os.getenv('BOT_NICK', 'CTFGameBot'),
        'username': os.getenv('BOT_USERNAME', 'CTFGameBot'),
        'realname': os.getenv('BOT_REALNAME', 'IRC CTF Game Bot'),
        'password': os.getenv('BOT_PASSWORD', 'your_secure_password_here'),
        'email': os.getenv('BOT_EMAIL', 'your_email@example.com'),
        'includes': [
            'irc3.plugins.core',
            'irc3.plugins.command',
            'irc3.plugins.cron',
            __name__,
        ],
        'autojoins': ['#CypherCon'],
        'debug': True,
    }

    # Create and run the bot
    bot = irc3.IrcBot(**config)
    bot.run(forever=True)

if __name__ == '__main__':
    main() 