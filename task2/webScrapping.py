import requests
from bs4 import BeautifulSoup

# Google News RSS feed URL
site = 'https://news.google.com/news/rss'

try:
    # Fetch data from the site
    response = requests.get(site)
    response.raise_for_status()  # Raise an error for HTTP issues

    # Parse the XML response
    sp_page = BeautifulSoup(response.content, 'xml')
    news_list = sp_page.find_all('item')  # Extract news items

    # Loop through each news item and display details
    for news in news_list[:10]:  # Limit output to 10 items
        print(f"Title: {news.title.text}")
        # print(f"Link: {news.link.text}")
        print(f"Published Date: {news.pubDate.text}")
        print('-' * 60)

except requests.exceptions.RequestException as e:
    print("Error fetching news:", e)
