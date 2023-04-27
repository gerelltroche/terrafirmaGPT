import os
import re
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import deque

URL = "https://1710-wiki.terrafirmacraft.com/"
visited_links = set()
sitemap = []

# Create a 'pages' folder if it doesn't exist
if not os.path.exists('pages'):
    os.makedirs('pages')

def is_wiki_page(url):
    # Check if the URL matches the pattern of a wiki page title
    wiki_page_pattern1 = re.compile(r'https://1710-wiki\.terrafirmacraft\.com/index\.php/([A-Za-z0-9_]+)$')
    wiki_page_pattern2 = re.compile(r'https:\/\/1710-wiki\.terrafirmacraft\.com\/([A-Za-z0-9_]+)$')
    return wiki_page_pattern1.match(url) or wiki_page_pattern2.match(url)

def save_page(url, content):
    page_name = url.split('/')[-1]
    file_path = os.path.join('pages', f"{page_name}.html")

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def scrape_links():
    queue = deque([URL])

    while queue:
        url = queue.popleft()
        response = requests.get(url)

        # Check if the content type is HTML
        content_type = response.headers.get('Content-Type')
        if content_type and 'html' not in content_type.lower():
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a', href=True):
            href = link['href']
            if not href.startswith('#'):  # Ignore internal page links
                full_url = urljoin(URL, href)
                if full_url.startswith(URL) and full_url not in visited_links:
                    visited_links.add(full_url)
                    sitemap.append(full_url)
                    print(full_url)
                    if is_wiki_page(full_url):
                        new_response = requests.get(full_url)
                        print("Saving:", href)
                        save_page(href, new_response.text)
                    queue.append(full_url)
                    time.sleep(2)  # Add a 2-second delay between requests

# I was considering making a sitemap, but consid
def main():
    print("Scraping links from", URL)
    scrape_links()

    print("\nSitemap:")
    with open('sitemap.txt', 'w', encoding='utf-8') as sitemap_file:
        for link in sitemap:
            sitemap_file.write(link + '\n')

if __name__ == "__main__":
    main()