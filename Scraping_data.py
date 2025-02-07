import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def scrape_books_data():
    # Data scrapping from 'books to scrape' website
    base_url = "http://books.toscrape.com/catalogue/"
    page_url = "http://books.toscrape.com/catalogue/page-1.html"

    book_titles = []
    prices = []
    ratings = []
    availability= []
    genres = []

    while page_url:
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find book buckets
        for book in soup.find_all("article", class_="product_pod"):
            # get book title
            title = book.h3.a["title"]
            book_titles.append(title)

            # get book price
            price = book.find("p", class_="price_color").text.replace("£","")
            prices.append(price)

            # get rating
            rating = book.p["class"][1]
            rating_mapped = {"One":1, "Two":2, "Three":3, "Four":4, "Five":5}
            ratings.append(rating_mapped[rating])

            # get availability
            availability_text = book.find("p", class_="instock availability").text.strip()
            availability.append("In stock" if "In stock" in availability_text else "Out of stock")

            # navigate to book details to get author and genre details
            book_url = base_url + book.h3.a["href"]
            book_response = requests.get(book_url)
            book_soup = BeautifulSoup(book_response.content, "html.parser")

            # get genre
            genre = book_soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
            genres.append(genre)

        # go to next page
        next_button = soup.find("li", class_="next")
        if next_button:
            page_url = base_url + next_button.a["href"]
        else:
            page_url = None

    # Converting to a DataFrame
    book_data = pd.DataFrame({
        "Book Title": book_titles,
        "Price (£)": prices,
        "Rating": ratings,
        "Availability": availability,
        "Genre": genres
    })
    print(book_data.head())
    print(book_data.tail())   

    book_data.to_csv("Book_Scraping_Analysis/scraped_books_data.csv", index=False)