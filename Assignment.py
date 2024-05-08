import requests
from bs4 import BeautifulSoup
import csv

def extract_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a', href=True)]
    return links

def extract_title_and_description(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('title').get_text()
    description = soup.find('meta', {'name': 'description'})
    description = description.get('content') if description else None
    return title, description

def main():
    # Extract links from dawn.com
    dawn_links = extract_links('https://www.dawn.com/')
    
    # Extract links from bbc.com
    bbc_links = extract_links('https://www.bbc.com/')
    
    # Extract titles and descriptions
    data = []
    for link in dawn_links + bbc_links:
        title, description = extract_title_and_description(link)
        if title and description:
            data.append({'title': title, 'description': description})
    
    # Store data in a CSV file
    with open('titles_and_descriptions.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(item)

if __name__ == "__main__":
    main()
