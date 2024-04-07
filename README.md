# Esilv_Api_Project

### Project
**Create an API for AI News Overview**

This project involves creating an API that provides news related to Artificial Intelligence (AI). Each group will select an AI-related site (e.g., OpenAI blog) as their source.

### Objective

The goal is to fetch information from the chosen site, either by scraping or through an existing API. You will create several endpoints for different purposes:

    - /get_data: Fetches a list of articles from the site. Retrieving 5 articles might be sufficient.
    - /articles: Displays information about the articles, including the article number, title, publication date, etc., but not the content itself.
    - /article/<number>: Accesses the content of a specified article.
    - /ml or /ml/<number>: Executes a machine learning script. Depending on the desired goal, it applies to either all articles or a single one. For example, sentiment analysis.

You can choose website about many subject like:

    - Updates on new AI tools.
    - News about image generation.
    - Information on new models.
    - Research papers, such as those from ArXiv or Google DeepMind.

### Process

    1. Each group should create a branch named after the names of the group members.
    2. Inside the branch, create a working directory named after the chosen site.
    3. Add a file named composition.txt that lists the members of the group.
    4. Add a section below these rules to explain your project, describe the created endpoints and their uses, and provide examples.


### Explications

Le endpoint get_data doit être appelé avant les autres pour récupérer les données du site actuia.com
Vous pouvez ensuite appeler les autres endpoints.

Même en forçant le codage en utf-8 les caractères spéciaux ne s'affiche pas correctement sur le navigateur cependant ils sont correctement décodés dans l'environnement python.
Cela ne nuit donc pas à l'étude des articles. 

On  utilise la bibliothèque TextBlob pour le ml et l'étude des sentiments, cela se base sur une liste de mots pré établies pour évaluer le sentiment général de l'article. 


### Explications du code Python global

Ce code Python est une application web construite avec Flask.

Fonctionnalités principales :
Endpoint /get_data : Récupère des articles à partir du site Web spécifié en utilisant BeautifulSoup pour analyser le HTML. Il extrait les liens des articles et récupère le titre, la date de publication et le contenu de chaque article. Les données sont stockées dans une liste d'articles.

Endpoint /articles : Renvoie une liste des articles disponibles, avec des informations telles que le numéro de l'article, le titre et la date de publication.

Endpoint /article/<number> : Accéder au contenu d'un article spécifique en fournissant son numéro. Si l'article existe, ses détails sont renvoyés ; sinon, un message d'erreur est retourné.

Endpoint /ml : Effectuer une analyse en utilisant du ML sur les articles. Elle peut être utilisée pour effectuer une analyse de sentiment ou d'autres traitements en fonction des besoins. L'analyse peut être effectuée sur tous les articles ou sur un article spécifique en fournissant son numéro.


Détails techniques :
Utilisation de Flask : Flask est utilisé comme framework principal pour gérer les requêtes HTTP et créer les différents points de terminaison.
Utilisation de BeautifulSoup : La bibliothèque BeautifulSoup est utilisée pour l'analyse HTML et l'extraction des données des articles à partir du site Web spécifié.
Stockage des données : Les données extraites des articles sont stockées dans une liste nommée articles.
Limitation du scraping : Le scraping est limité aux premiers 10 articles trouvés sur le site pour des raisons de performance et pour éviter de surcharger le serveur distant.
Gestion des délais : L'application utilise des délais aléatoires entre les requêtes pour éviter d'être bloquée par le site Web cible en cas de demandes trop fréquentes, ce qui peut être considéré comme une activité de type "bot" et entraîner le blocage de l'adresse IP.
