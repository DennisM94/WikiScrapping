import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, CheckButtons

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

def remove_stop_words(word_counts):
    stop_words = [
        "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in",
        "into", "is", "it", "no", "not", "of", "on", "or", "such", "that", "the",
        "their", "then", "there", "these", "they", "this", "to", "was", "will",
        "with", "s", "ger", "o", "de", "do", "ce", "da", "c", "e", "m", "p", "from", "b"
    ]
    return Counter({word: count for word, count in word_counts.items() if word not in stop_words})

def plot_word_count_bar(counter, n=10):
    top_n = counter.most_common(n)
    labels, values = zip(*top_n)
    plt.bar(labels, values)
    plt.xlabel("Words")
    plt.ylabel("Occurrences")
    plt.title("Top {} Words in Wikipedia Article (Bar Chart)".format(n))

def plot_word_count_pie(counter, n=10):
    top_n = counter.most_common(n)
    labels, values = zip(*top_n)
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title("Top {} Words in Wikipedia Article (Pie Chart)".format(n))

def draw_chart(chart_type, word_counts):
    plt.clf()
    word_counts = remove_stop_words(word_counts)
    if chart_type == "bar":
        plot_word_count_bar(word_counts)
    elif chart_type == "pie":
        plot_word_count_pie(word_counts)
    plt.subplots_adjust(bottom=0.2)
    plt.draw()

def on_bar_click(event, word_counts):
    draw_chart("bar", word_counts)

def on_pie_click(event, word_counts):
    draw_chart("pie", word_counts)

def on_check_update(label, state, word_counts, chart_type):
    if label == "Filter Stop Words":
        draw_chart(chart_type, word_counts, state)

def main():
    url = input("Enter the Wikipedia article URL: ")

    html = fetch_wikipedia_article(url)
    text = extract_text_from_html(html)
    cleaned_text = clean_text(text)

    common_words = ["the", "a", "an", "in", "on", "of", "for", "to", "and", "is", "was", "were", "are"]
    cleaned_text = " ".join([word for word in cleaned_text.split() if word not in common_words])
    
    word_counts = count_words(cleaned_text)

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.2)
    draw_chart("bar", word_counts)

    bar_ax = plt.axes([0.3, 0.05, 0.2, 0.075])
    pie_ax = plt.axes([0.5, 0.05, 0.2, 0.075])

    bar_button = Button(bar_ax, "Bar Chart")
    bar_button.on_clicked(lambda event: on_bar_click(event, word_counts))
    pie_button = Button(pie_ax, "Pie Chart")
    pie_button.on_clicked(lambda event: on_pie_click(event, word_counts))

    plt.show()

if __name__ == "__main__":
    main()
