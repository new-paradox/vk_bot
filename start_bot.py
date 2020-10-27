from bot import Bot

try:
    import config
except ImportError:
    exit('DO cp config.py.default config.py and set token')

if __name__ == '__main__':
    bot = Bot(id_group=config.GROUP_ID, token_=config.TOKEN)
    bot.run()
