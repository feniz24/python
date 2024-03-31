import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"
response = requests.get(URL)
website_data = response.text
# print(website)

soup = BeautifulSoup(website_data, "html.parser")
# website = soup.prettify()
# print(website)

title_links = soup.find_all(name="h3", class_="title")
# print(title_links)
titles = [link.getText() for link in title_links]

titles_list = titles[::-1]
# print(titles_list)

with open("top_100_movies.txt", "w") as file:
    for title in titles_list:
        file.write(f"{title} \n")