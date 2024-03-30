import smtplib
import datetime as dt
import random

my_email = ""
password = ""

now = dt.datetime.now()
date_of_week = now.weekday()


if date_of_week == 0:
    with open("quotes.txt") as data_file:
        quotes = data_file.readlines()
    quote = random.choice(quotes)
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=my_email,
                            msg=f"Subject:Monday Motivation\n\n{quote}")
