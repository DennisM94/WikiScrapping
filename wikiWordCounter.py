import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import matplotlib.pyplot as plt

def fetch_wikipedia_article(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch the article: {response.status_code}")

    return response.text

def extract_text_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
    text = soup.get_text()
    return text

def clean_text(text):
    return re.sub('[^A-Za-z]+', ' ', text.lower()).strip()

def count_words(text):
    words = text.split()
    return Counter(words)

def plot_word_count(counter, n=10):
    top_n = counter.most_common(n)
    labels, values = zip(*top_n)
    plt.bar(labels, values)
    plt.xlabel("Words")
    plt.ylabel("Occurrences")
    plt.title("Top {} Words in Wikipedia Article".format(n))
    plt.show()

def main():
    url = input("Enter the Wikipedia article URL: ")
    html = fetch_wikipedia_article(url)
    text = extract_text_from_html(html)
    cleaned_text = clean_text(text)
    word_counts = count_words(cleaned_text)
    plot_word_count(word_counts)

if __name__ == "__main__":
    main()
