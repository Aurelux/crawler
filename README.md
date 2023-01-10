# TP1 - crawler minimal

Bertail Aurélien

## Description des fichiers 

### main.py

fichier avec le code python du crawler

### Crawled_webpages.txt

Exemple des 50 sites web scrollés depuis https://ensai.fr

### fichier .sqlite

Base de données relationelle de l'ensemble des sites web trouvées avec leur age( profondeur)

## Description du code

Ce code est un crawler single-threaded.
À partir d'une URL d'entrée unique (ici https://ensai.fr/), le crawler télécharge une page, puis
attend au moins cinq secondes avant de télécharger la page suivante. Le programme analyse les fichiers robots.twt et sitemap.xml des sites webs téléchargés afin de trouver d'autres url a explorer tout en respectant la politness et en ne crwlant uniquement les sites autorisés.

Le programme se termine lorsque le crawler arrive à 50 urls trouvées ou si il ne trouve
plus de liens à explorer.
Une fois terminé, le programme écrit dans un fichier crawled_webpages.txt toutes les urls
trouvées. Il stocke également l'ensmeble des urls trouvées dans une base de données SQlite.

Il y a egalement une petite fonction de test qui permet de scrawl deux sites xeb et de verifier que le scrawl se passe bien et que la bdd n'est pas vide


## Éxécuter le code

Afin d'éxecuter le code, il suffit de lancer le lacer le fichier main.py sur son ordinateur, il faut au préalable installer l'ensemble des packages nécéssaires. Pour changer d'url de départ, il suffit de modifier la varibale "url" a la fin de la page main.py

Pour tester le code il faut retirer les ''' du code et lancer le main.py, le test va alors s'effectuer.



