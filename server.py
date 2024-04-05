from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

articles = []

@app.route('/get_data', methods=['GET'])
def get_data():
    global articles
    url = "https://www.artificialintelligence-news.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    article_elements = soup.find_all('h3', class_='entry-title td-module-title')[:10]
    articles = [
        {
            'number': i+1, 
            'title': article.find('a').get_text(strip=True), 
            'publication_date': datetime.now().strftime('%Y-%m-%d'), 
            'content': article.find('a')['href']
        } 
        for i, article in enumerate(article_elements)
    ]
    return jsonify({'message': 'Data fetched successfully', 'articles_fetched': len(articles)})

@app.route('/articles', methods=['GET'])
def list_articles():
    return jsonify([{'number': article['number'], 'title': article['title'], 'publication_date': article['publication_date']} for article in articles])

@app.route('/article/<int:number>', methods=['GET'])
def get_article(number):
    article = next((article for article in articles if article['number'] == number), None)
    if article:
        return jsonify(article)
    else:
        return jsonify({'message': 'Article not found'}), 404

@app.route('/ml', defaults={'number': None}, methods=['GET'])
@app.route('/ml/<int:number>', methods=['GET'])
def ml_analysis(number):
    if number is None:
        return jsonify({'message': 'ML analysis for all articles'})
    else:
        article = next((article for article in articles if article['number'] == number), None)
        if article:
            return jsonify({'message': f'ML analysis for article {number}'})
        else:
            return jsonify({'message': 'Article not found for ML analysis'}), 404

if __name__ == '__main__':
    app.run(debug=True)
