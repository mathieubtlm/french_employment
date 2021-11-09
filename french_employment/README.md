----------------------------------------------------------------------------------------------------------------------------------------------------

				##Table des matières


 	- [Introduction](##Introduction)
 	- [User Guide](##users-Guide)
 	- [Developer Guide](##developers-Guide)
 	- [Lien vers les datasets](##lien-vers-les-datasets)
 	- [Instructions d'execution](##instructions-dexecution)
	- [Rapport d'analyse](##Rapport d'analyse)


----------------------------------------------------------------------------------------------------------------------------------------------------


				## Introduction


	Ce dashboard a pour but de visualiser les différentes composantes de l'emploi en France.
	On essaiera d'estimer la répartion des salaires, l'existence d'écarts salariales hommes / femmes,
	la répartition des entreprises en France Métropolitaine.


----------------------------------------------------------------------------------------------------------------------------------------------------

				## User Guide
		
	On propose à l'utilisateur de visualiser les données avec Python et sa librairie dash.
	Pour executer ce code sans erreur,on doit d'abord le récupérer le dossier sur github.
	Ensuite, il faut installer tous les packages, en tapant dans
	l'invite de commande: pip install le_nom_du_package.

	liste des librairies/packages utilisés:
	- dash
	- folium
	- geopandas
	- numpy
	- branca.colormap
	- plotly.express
	- plotly.graph_objs
	

	geopandas nécessite l'installation de dépendances. Dans le cas où son installation pose problème,
	cette courte vidéo explique comment proprement résoudre ce problème:
	https://www.youtube.com/watch?v=H1A5mZDoXYg
	
	Lorsque les packages sont installés, on doit dans le terminal se placer dans le répertoire où se trouve
	le fichier main.py. Ensuite, il suffit d'executer la commande: **python main.py**
	Après quelque secondes, le dashboard est visible à l'adresse http://127.0.0.1:8050/ .


----------------------------------------------------------------------------------------------------------------------------------------------------

				## Developper Guide


	Ce guide mentionne l'architecture et les fonctions utiles du projet et les éventuelles pistes de développement.

	Architecture du projet:

	Le projet est décomposé en 6 fichiers:

	-  main.py (Lance les fonctions principales, initialise l'application, lance le serveur dash)
	-  README.md (Instructions et rapport du projet)
	-  base_etablissement_par_tranche_effectif.csv (contient des données sur les entreprises)
	-  name_geographic_information.csv (contient des données geographiques)
	-  net_salary_per_town_categories.csv (contient des données sur les salaires)
	-  map.html (La carte, qui se crée au lancement de l'application)




	Les différentes fonctions du projet:

	> - import_clean()
	Crée et retourne (companies, geoinf, salaries, dep, firm_val, geo_dep, firmlog), qui vont nous servir pour la carte et pour les plots.


	> - dataframe()
	Creation/update des dataframe, pour qu'ils aient le bon format pour nos autres fonctions. Retourne (firm, geo_dep, colormap, wage_gap).
	Tous sont des DataFrame, sauf colormap qui est un branca.colormap.StepColormap.


	> - chloro_map()
	Creation de notre carte, qui sera créee et stockée dans un fichier html avant d'être réutilisée. Ne retourne rien.


	> - bar_plot()
	Creation d'un bar plot regroupant les salaires horaires en fonction des différents postes. Retourne une figure (fig)
	de type plotly.graph_objs._figure.Figure.


	> - dashboard()
	Création du dashboard avec dash et affichagee des différents éléments. Ne retourne rien.


	> - update_graph(option_slctd)
	Fonction permettant l'update de l'histogramme. Elle prend en argument l'age choisi(chaine de caractères).
	Retourne une liste contenant notre figure (histogramme, de type)


	> - main()
	Fonction permettant de lancer les fonctions principales
	


----------------------------------------------------------------------------------------------------------------------------------------------------
	

	Lien vers le dataset: https://www.kaggle.com/etiennelq/french-employment-by-town


----------------------------------------------------------------------------------------------------------------------------------------------------

	Instructions d'execution:
	- Télécharger le dossier french_employment
	- Le dézipper
	- Ouvrir l'invite de commande
	- Se déplacer dans les répertoires afin que le répertoire courant soit french_employment
	- Lancer la ligne de commande suivante dans le terminal: ** python main.py **
	- Après quelque secondes, le dashboard est visible à l'adresse http://127.0.0.1:8050/ .
	

----------------------------------------------------------------------------------------------------------------------------------------------------

			## Rapport d'analyse

	On fait part dans ce rapport de nos hypothèses, basées sur le dashboard et sur ce qu'on peut en tirer.	

	On commence par "Répartition des salaire à l'heure en fonction de l'age".

	Le Dropdown nous permet de sélectionner l'age que l'on veut voir affiché.
	En changeant l'âge, on constate que le salaire horaire moyen augmente globalement avec l'âge, ce qui est assez logique.
	Il y a en effet souvent une corrélation entre le salaire et les années d'expériences.
	De plus, le nombre de données semble augmenter lorsque l'on quitte la tranche 18-25 ans: en effet, de nombreuses
	personnes font des études ou autre à cet âge là et ne sont pas encore dans la vie active. Ils ont d'ailleurs sûrement un emploi étudiant,
	ce qui expliquerait le pic de salaire autour d'environ 9 chez les 18-25 ans.


	Ensuite, on va observer les "Ecarts salariales Homme-Femme sur les différentes villes".
	
	Sur la figure, on constate que certaines villes ont un écart salarial plutôt bas, parfois avoisinant le 0 avec des valeurs comme
	0.3, 0.5 ou même 0.1, mais sauf pour quelques rares cas, les hommes gagnent plus que les femmes dans la plupart des villes
	d'après cette figure.
	De plus, on constate quasi systématiquement une augmentation de l'écart salarial lorsque l'on sélectionne une ville avec des revenus
	horaires supérieurs à d'autres, et ce de mannière quasi proportionnel. Pour la plupart des pics bleus, on constate des pics rouge.
	On pourrait interpreter ça par le fait que lorsqu'une ville à un salaire horaire élevé, l'écart salarial suit dans la majorité des cas.
	Il pourrait éventuellement être intéressant de récupérer l'index des villes ayant un écart salarial négatif (soit les femmes qui
	gagnent plus que les hommes) pour tenter d'établir un lien entre ces dernières et expliquer ce phénomène, bien qu'elles soient 
	en forte infériorité, et qu'elle soient de l'ordre de 0.2 lorsqu'elles existent.


	À présent, on observe la figure "Salaires moyens en fonction du poste".

	Au premier coup d'oeil, on remarque que pour chaque poste le salaire horaire des hommes est en moyenne plus élevé.
	L'écart semble augmenter avec les responsabilités, ce qui semble être en accord avec les observations précédentes.


	Enfin, on observe le "Nombre de firmes par départements".

	Cette carte nous permet d'obtenir plusieurs informations. Avec ce code couleur judicieusement choisi, on peut
	grossièrement repérer ce qu'on appelle "la diagonale du vide". En outre, le nombre de firmes par départements semble augmenter et 
	suivre la démographie, chose qui pourrait être vérifier avec l'ajout d'une autre carte sur la répartition de la population.	
	On remarque que les départements ayant le plus de firmes contiennent les grandes métropoles (Nantes, Bordeaux, Montpellier, Marseille,
	Paris, Grenoble, Lille...).
	Par ailleurs, on remarque que l'Ile-De-France, au centre de la figure, regroupe des départements avec un nombre de firmes globablement
	élevé. Toutefois, parmis ces derniers, les Hauts-de-Seine (92) se distingue et se hisse au même rang que les métropoles.
	Cela pourrait s'expliquer en partie avec l'existence du quartier d'affaires de La Défense et de sa proximité avec Paris.
	Cette dernière se distingue totalement de tout le reste de la figure, avec un nombre de firmes 3 à 4 fois plus élevé que les grandes
	métropoles, malgré sa surface assez réduite. C'est bien évidemment car Paris représente le centre économique du pays.










	