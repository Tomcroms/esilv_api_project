from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import time
import random
from textblob import TextBlob


app = Flask(__name__)

articles = []

@app.route('/get_data', methods=['GET'])
def get_data():
    global articles
    articles = []

    base_url = "https://www.actuia.com/"
    url = base_url
    response = requests.get(url)
    response.encoding = 'utf-8'

    time.sleep(random.uniform(1, 2))
    soup = BeautifulSoup(response.text, 'html.parser')


    a_elements = soup.find_all('a', href=True)
    
    
    filtered_a_elements = [a for a in a_elements if "actualite" in a['href']]

    i=0
    for a in filtered_a_elements:
        i+=1
        if(i>10):
            break
        article_url = a['href']
        
        article_response = requests.get(article_url)
        article_soup = BeautifulSoup(article_response.text, 'html.parser', from_encoding='utf-8')

        
        h1 = article_soup.find('h1')
        author_name_span = article_soup.select_one('span[class*="author-name"]')
        if h1 and author_name_span:
            title = h1.text
            previous_span = author_name_span.find_previous_sibling('span')

            if previous_span:
                publication_date = previous_span.text
            else:
                publication_date = "No publication_date for this article"
            article_element = article_soup.find('article')
            paragraphs = article_element.find_all('p') if article_element else []
            content = ' '.join(p.get_text(strip=True) for p in paragraphs)

            articles.append({
                'title': title,
                'publication_date': publication_date,
                'content': content,
                'url': article_url
            })

    response = jsonify({'message': 'Données récupérées avec succès', 'articles': articles})
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response


@app.route('/articles', methods=['GET'])
def list_articles():
    global articles
    articles_info = [{
        'number': i + 1,
        'title': article['title'],
        'publication_date': article['publication_date'],
        'url': article['url']
    } for i, article in enumerate(articles)]

    response = jsonify({'message': 'Liste des articles', 'articles': articles_info})
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response


@app.route('/article/<int:number>', methods=['GET'])
def get_article(number):
    global articles
    if 1 <= number <= len(articles):
        article = articles[number - 1]
        article_data = {
            'title': article['title'],
            'publication_date': article['publication_date'],
            'content': article['content'],
            'url': article['url']
        }
        response = jsonify({'message': 'Article trouvé', 'article': article_data})
    else:
        response = jsonify({'message': 'Article non trouvé', 'error': 'Invalid article number'})
        response.status_code = 404

    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.route('/ml', defaults={'number': None})
@app.route('/ml/<int:number>', methods=['GET'])
def analyze_sentiment(number):
    global articles
    if number is None:
        # Applique l'analyse de sentiment à tous les articles
        sentiments = []
        for article in articles:
            analysis = TextBlob(article['content'])
            sentiments.append({
                'title': article['title'],
                'sentiment': analysis.sentiment.polarity
            })
        response = jsonify({'message': 'Analyse de sentiment pour tous les articles', 'sentiments': sentiments})
    else:
        # Applique l'analyse de sentiment à un article spécifique
        if 1 <= number <= len(articles):
            analysis = TextBlob(articles[number - 1]['content'])
            response = jsonify({
                'title': articles[number - 1]['title'],
                'sentiment': analysis.sentiment.polarity,
                'message': 'Analyse de sentiment pour l\'article spécifié'
            })
        else:
            response = jsonify({'message': 'Article non trouvé', 'error': 'Invalid article number'})
            response.status_code = 404

    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

if __name__ == '__main__':
    app.run(debug=True)
