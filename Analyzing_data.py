import os
import pandas as pd
from Scraping_data import scrape_books_data
import seaborn as sns
import matplotlib.pyplot as plt

# Check if the data file exists
file_name = "Book_Scraping_Analysis/scraped_books_data.csv"
if os.path.exists(file_name):
    # Load existing data
    print("Loading data...")
    book_data = pd.read_csv(file_name)
else:
    # Scrape data
    print("Scraping data...")
    book_data = scrape_books_data() 

print(book_data.head())

# Step 1: Data cleaning
# Check price stats
print("Highest price", book_data["Price (£)"].max())
print("Lowest price", book_data["Price (£)"].min())

# create buckets based on price range
price_range = book_data["Price (£)"].max() - book_data["Price (£)"].min()
bucket_size = price_range / 4
bins = [book_data['Price (£)'].min(), 
        book_data['Price (£)'].min() + bucket_size, 
        book_data['Price (£)'].min() + 2 * bucket_size, 
        book_data['Price (£)'].min() + 3 * bucket_size, 
        book_data['Price (£)'].max()]
labels = ["Very Low", "Low", "Medium", "High"]

# Add price category to dataframe based on buckets
book_data["Price Category"] = pd.cut(book_data['Price (£)'], bins=bins, labels=labels)
print(book_data.head())


# Step 2: Analysis and Insights
# Grouped Analysis: Average Rating by Genre
genre_rating_summary = book_data.groupby("Genre")["Rating"].mean().sort_values(ascending=False)
print("Average Ratings by Genre:\n", genre_rating_summary)


# Step 3: Visualization in Python
# Average Rating by Genre
plt.figure(figsize=(12,8))
sns.barplot(y=genre_rating_summary.index, x=genre_rating_summary.values, palette="viridis")
plt.title("Average Rating by Genre")
plt.xlabel("Average Rating")
plt.ylabel("Genre")
plt.show()

# Top 10 Genres by Number of Books
plt.figure(figsize=(10,6))
top_genres = book_data['Genre'].value_counts().head(10)
sns.barplot(x=top_genres.values, y=top_genres.index, palette="muted")
plt.title("Top 10 Genres by Number of Books")
plt.xlabel("Number of Books")
plt.ylabel("Genre")
plt.show()

# Price Distribution by Genre
plt.figure(figsize=(12,10))
sns.boxplot(x="Genre", y="Price (£)", data=book_data)
plt.xticks(rotation=90)
plt.title("Price Distribution by Genre")
plt.show()


# Step 4: Export to Excel
book_data.to_excel("Book_Scraping_Analysis/cleaned_books_data.xlsx", index=False)
