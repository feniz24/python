from bs4 import BeautifulSoup
import requests
import smtplib

MY_EMAIL = ""
target_price = 350.0
product_url = "https://www.amazon.com/Sony-WH-1000XM5-Canceling-Headphones-Hands-Free/dp/B09XS7JWHH/ref=sr_1_2?dib=eyJ2IjoiMSJ9.VnkfPbuolzxpLc7ybu03bapUq9oaAuJ4HgxgR5n0nDwDlQqzO_Nia9-BInkIShb75ro8-5uR-zSzitY_f2kSW6tioubcTqSfm_Xtm86W-7tTFl0PQ8QEN161saLR-68QWNSDNGkv8gAhWJGFq-7HcmPXFx8I5evM68rXU_nUBU5gnvikd0905bJpADpRciRpAHPd3kqixTV6BIG_WzCxSD7ZTFhyNFU7aHfJJQdoRiQ.NDm9QurlZfoh7T8dw1d-tGAz9h0HEYpJ0Kahmkk6t7Y&dib_tag=se&keywords=sony%2Bwh-1000xm5&qid=1711858066&sr=8-2&th=1"
headers = {
    "Accept-Language": "",
    "User-Agent": "",
}

response = requests.get(product_url, headers=headers)
website_data = response.text

soup = BeautifulSoup(website_data, 'lxml')
price = float(soup.find(name="span", class_="a-price-whole").getText().split('.')[0])

if price < target_price:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password="")
        connection.sendmail(from_addr="",
                            to_addrs="",
                            msg=f"Subject:Discount Alert\n\nDiscount is coming. Grab one")
