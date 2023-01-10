import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
import time
import sqlite3





# Connexion à la base de données
connection = sqlite3.connect("crawler_database.sqlite")
cursor = connection.cursor()

#creation de la base de donnée qui va stocker les url et leur age (profonfeur de la recherche)
cursor.execute("CREATE TABLE IF NOT EXISTS pages (url TEXT, profondeur INT)")

#fonction de crawl, on fixe le nombre de page limite et et delay entre les recherches pour respecter la politness

def crawl(url, page_limit = 50,delay=2):
    number_page = 0 #nombre de pages visitées
    pages_visited = []#liste des pages visitées afin d'éviter de revenir sur la meme page
    pages_to_visit = [url] #liste des pages à visiter

    #On regarde le fichier robots afin de voir quels sont les url nous pouvons visiter.
    rp = RobotFileParser()
    rp.set_url(f"{urlparse(url).scheme}://{urlparse(url).hostname}/robots.txt")
    rp.read()

    #On lit également el fichier site map pour augmenter le nombre de site a visiter
    sitemap = requests.get(f"{url}/sitemap.xml").text
    soup = BeautifulSoup(sitemap, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('http') and rp.can_fetch("*", href) and href not in pages_visited: #on verifie qu'on peut y acceder, que l'url est correct et que l'on a pas visiter le site auparavant
            pages_to_visit.append(href)

    #On ouvre alors le fichier text ou l'on va stocker les sites web que l'on a visité
    with open("crawled_webpages.txt", "w") as f:
        while number_page < page_limit and pages_to_visit: #tant qu'il y a encore des pages a visiter et que le nombre de pages visitées maximum n'est pas atteint on continue
            current_page = pages_to_visit.pop(0)
            if current_page in pages_visited: #si deja visitée alors on continue et on recommence
                continue
            if not rp.can_fetch("*", current_page):#de meme si la page n'est pas autorisée
                continue
            pages_visited.append(current_page) #on rajoute la page dans les pages visitées
            # Effectue une requête GET sur l'URL spécifiée
            response = requests.get(current_page)
            number_page += 1 #on rajoute +1 au nombre de pages visitées
            f.write(current_page+"\n") #on rajoute le lien sur le fichir text de sortie
            # Parsing du HTML de la réponse
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extraction des liens
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and href.startswith('http') and rp.can_fetch("*", href) and href not in pages_visited: #on enlève les liens ne commencant pas par http
                    pages_to_visit.append(href)
            print(f'Pages visited: {number_page}, Pages to visit: {len(pages_to_visit)}')
            time.sleep(delay) #on rajoute un delais pour la politesse
            for pages_web in pages_to_visit : 
                cursor.execute("INSERT INTO pages VALUES (?,?)", (pages_web, number_page)) #On rajoute l'ensemble des pages trouvées avec leur age dans la base de données
                connection.commit()
    print("crawling done, check crawled_webpages.txt for result") #message s'affichant à la fin du script

#Fonction de test pour tester la fonction crawl
import unittest
from unittest.mock import patch

class TestCrawler(unittest.TestCase):
    @patch('requests.get')
    def test_visit_page(self, mock_get):
        # Arrange
        mock_get.return_value.text = "<html><a href='http://example.com/page1'>Page 1</a></html>"
        # Act
        crawl('http://example.com')
        # Assert
        cursor.execute("SELECT * FROM pages WHERE url = 'http://example.com/page1'")
        result = cursor.fetchone()
        self.assertIsNotNone(result) #on regarde si la bdd n'est pas nulle

# Utilisation de la fonction de test
#il faut enlver les guillemets su l'on souhaite tester le code
'''
if __name__ == '__main__':
    unittest.main()
'''

    
# Utilisation de la fonction : on choisit l'url et on lance la fonction
url = 'https://ensai.fr/'
crawl(url)
