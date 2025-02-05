import requests
from bs4 import BeautifulSoup
import json

# Function to fetch data from Reddit using API


# Function to fetch data from Medium (using scraping)
def fetch_medium_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    url = 'https://medium.com'  # You may need to change the URL depending on your exact scraping target
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        posts_data = []

        # Extract the text and engagement (likes or responses)
        for article in soup.find_all('article'):
            text = article.get_text()
            engagement = 1000  # In reality, scrape likes/comments, this is a placeholder

            posts_data.append({
                "text": text.strip(),
                "engagement": engagement
            })
        return posts_data
    else:
        print("Error fetching Medium data")
        return []


# Function to fetch data from The New York Times (using scraping)
def fetch_nyt_data():
    url = 'https://www.nytimes.com'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        posts_data = []

        for article in soup.find_all('article'):
            text = article.get_text()
            engagement = 1500  # Placeholder for engagement, this would depend on the article
            posts_data.append({
                "text": text.strip(),
                "engagement": engagement
            })

        return posts_data
    else:
        print("Error fetching NYT data")
        return []


# Function to fetch data from The Atlantic (using scraping)
def fetch_atlantic_data():
    url = 'https://www.theatlantic.com'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        posts_data = []

        for article in soup.find_all('article'):
            text = article.get_text()
            engagement = 1200  # Placeholder engagement
            posts_data.append({
                "text": text.strip(),
                "engagement": engagement
            })

        return posts_data
    else:
        print("Error fetching Atlantic data")
        return []


# Function to fetch data from Wired (using scraping)
def fetch_wired_data():
    url = 'https://www.wired.com'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        posts_data = []

        for article in soup.find_all('article'):
            text = article.get_text()
            engagement = 1100  # Placeholder engagement
            posts_data.append({
                "text": text.strip(),
                "engagement": engagement
            })

        return posts_data
    else:
        print("Error fetching Wired data")
        return []


# Function to fetch data from Farnam Street (using scraping)
def fetch_farnam_street_data():
    url = 'https://fs.blog'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        posts_data = []

        for article in soup.find_all('article'):
            text = article.get_text()
            engagement = 900  # Placeholder engagement
            posts_data.append({
                "text": text.strip(),
                "engagement": engagement
            })

        return posts_data
    else:
        print("Error fetching Farnam Street data")
        return []


# Main function to collect all posts and save to JSON
def collect_data_and_save_to_json(output_file='scraped_posts.json'):
    all_posts = []

    # Fetch data from different sources
    all_posts.extend(fetch_medium_data())
    all_posts.extend(fetch_nyt_data())
    all_posts.extend(fetch_atlantic_data())
    all_posts.extend(fetch_wired_data())
    all_posts.extend(fetch_farnam_street_data())

    # Save the scraped posts to a JSON file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(all_posts, file, indent=4, ensure_ascii=False)


# Run the scraping and saving process
if __name__ == "__main__":
    collect_data_and_save_to_json()
