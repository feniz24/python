from InstaFollower import InstaFollower
import time

bot = InstaFollower()

bot.login()
bot.find_followers()
bot.follow()

time.sleep(30)
