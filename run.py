from slackbot.bot import Bot
import slackbot_settings
from slacker import Slacker

def main():
    bot = Bot()
    
    slack = Slacker(slackbot_settings.API_TOKEN)
    slack.chat.post_message('bot', 'Run SlackBot!!', as_user=True)

    bot.run()

if __name__ == '__main__':
    main()