from InternetSpeedTwitterBot import InternetSpeedTwitterBot

bot = InternetSpeedTwitterBot()

speed = bot.get_internet_speed()

bot.tweet_at_provider(speed)