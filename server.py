from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import time
import random

app = Flask(__name__)

articles = []


# Récupère une liste d'articles sur le site de actuia
@app.route('/get_data', methods=['GET'])
def get_data():
    global articles
    articles = []

    base_url = "https://www.actuia.com/"
    url = base_url
    response = requests.get(url)

    time.sleep(random.uniform(1, 2))
    soup = BeautifulSoup(response.text, 'html.parser')


    a_elements = soup.find_all('a', href=True)
    
    
    filtered_a_elements = [a for a in a_elements if "actualite" in a['href']]
    print(filtered_a_elements)

    i=0
    for a in filtered_a_elements:
        print(i)
        i+=1
        if(i>10):
            break
        article_url = a['href']
        
        article_response = requests.get(article_url)
        article_soup = BeautifulSoup(article_response.text, 'html.parser')

        
        h1 = article_soup.find('h1')
        if h1:
            print("h1")
            title = h1.get_text(strip=True)
            articles.append({
                'title': title
            })


            publication_date =  "a faire"
            article_element = article_soup.find('article')
            paragraphs = article_element.find_all('p') if article_element else []
            content = ' '.join(p.get_text(strip=True) for p in paragraphs)

            articles.append({
                'title': title,
                'publication_date': publication_date,
                'content': content,
                'url': article_url
            })

    return jsonify({'message': 'Données récupérées avec succès', 'articles': articles})

# Affiche des informations sur les articles (numéro, titre, date de publication)
@app.route('/articles', methods=['GET'])
def list_articles():
    return jsonify([{'number': article['number'], 'title': article['title'], 'publication_date': article['publication_date']} for article in articles])


# Accède au contenu d'un article spécifié (avec son numéro)
@app.route('/article/<int:number>', methods=['GET'])
def get_article(number):
    article = next((article for article in articles if article['number'] == number), None)
    if article:
        return jsonify(article)
    else:
        return jsonify({'message': 'Article not found'}), 404


# ML analysis
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
