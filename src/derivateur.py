#!/usr/bin/python
# coding=latin-1
from bs4 import BeautifulSoup
import urllib.request
import csv
import sys
from nltk import word_tokenize , sent_tokenize 
import re
from pprint import pprint



resultat={}


#fonction qui à partir du mot rentré en paramètres et le fichier regles.txt génère un ensemble de mots dérivés.
def derivationTerme(mot):
	global resultat
	fichier = open("regles.txt", "r", encoding='utf8')

	i =0
	tempo=[]
	with open("regles.txt", "r") as fichier:
		for line in fichier.readlines():
			tempo.append(line.rstrip('\n').split("==>"))

	fichier.close()


	suffixes=[]
	while i < len(tempo) :
		suff=tempo[i][0].split(":")
		m = tempo[i][1].split(":")
		for s in suffixes:
			if s.endswith(suff[1]) and s!=suff[1]:
				i+=1
			
		if mot.endswith(suff[1]) and len(suff[1]) !=0:
			suffixes.append(suff[1])
			mt=mot[:-len(suff[1])]
			if mt != suff[1]:
				nvMot= mt + m[1]
				if not (nvMot in resultat):
					resultat[nvMot] = m[0]
		if len(suff[1])==0:
			resultat[mot + m[1]] = m[0]
		i+=1



#fonction qui vérifie si la relation (entrante ou sortante) entre un mot d'origine et un mot dérivé existe.
#C-a-d: si le poids de la relation est positif alors nous retournons "True", sinon on retourne "False".
def verificationRelation(relation, idMotOrigine, idMotRecup):

	j=2
	while j < len(relation):
		s=relation[j].split(";")
		if len(s)>2:
			if s[2]==idMotOrigine:
				if s[3]==idMotRecup:
					if int(s[-1]) > 0 :
						return True
			else:
				if s[2]==idMotRecup:
					if s[3]==idMotOrigine:
						if int(s[-1]) >0 :
							return True
		j+=1

	return False



#Les relations que nous utilisons pour générer les mots en relation avec le mots d'origine à partir de JDM (Resodump).
relations=['43', '44', '65', '99', '159', '160', '164', '165', '22','39', '40']
terme= input('veuillez entrer un terme:')





#Fonction qui génére à partir du mot rentré en paramètre, un ensemble de mots dérivé de ce dernier en utilisant les relation ci-dessus de JDM.
motsRezoDump=[]
def generationMotsJDM():


	for i in relations: 
		#Accès à JDM avec le mot d'origine et le noméro de la relation.
		urlpage = u'http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel='+terme+'&rel='+i
	
		page = urllib.request.urlopen(urlpage)
		soup = BeautifulSoup(page, "lxml")

		code= soup.find("code")
		if code:
			result=code.get_text()
			tempo=result.split("//")
			postag=tempo[3].split("\n")
			idMotGenere=postag[2].split(";")[1]
		

			i=3
			while i <len(postag):
				r=postag[i].split(";")
				if len(r)>2:
					idRecup=r[1].replace(":","").replace("'","")
					motRecup=r[2].replace(":","").replace("'","")
				
					#S'il existe une relation sortante avec un poids positif, on ajoute le mot dérivé à la liste.
					relationSortante=tempo[5].split("\n")
					if verificationRelation(relationSortante, idMotGenere, idRecup) and motRecup not in motsRezoDump and motRecup != terme:
						motsRezoDump.append(motRecup)
					#Sinon, s'il existe entre les deux mots une relation entrante.
					else:
						relationEntrante=tempo[6].split("\n")
						if verificationRelation(relationEntrante, idMotGenere, idRecup) and motRecup not in motsRezoDump and motRecup != terme:
							motsRezoDump.append(motRecup)


				i+=1


	
	#On retourne l'ensemble des mots que JDM a généré.
	return motsRezoDump




#Pour l'ensemble des mots que nous avons généré et vérifié l'existence dans JDM, on vérifie si la nature que nous leur avons
#attribuéé est correcte.
def verificationNature(motsValides):

	for key, value in motsValides.items():
		k=key.encode('latin-1')
		quoted = urllib.parse.quote(k)
		urlpage = u'http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel='+quoted+'&rel=4'


		page = urllib.request.urlopen(urlpage)
		soup = BeautifulSoup(page, "lxml")
		poids={}
		code= soup.find("code")
		if code:
			result=code.get_text()
			tempo=result.split("//")
			postag=tempo[3].split("\n")
			i=2
			nat=False
			while i <len(postag):
				r=postag[i].split(";")

				if len(r)>2:
					nature=r[2].replace(":","").replace("'","")
					identifiantRelation=r[1]

					poids[identifiantRelation]=[]

					poids[identifiantRelation].append(nature)

					if nature==value and r[3]=="4":
						nat=True

				i+=1
				
			relationSortante=tempo[5].split("\n")
			j=2
			while j<len(relationSortante):
				c=relationSortante[j].split(";")	
				if len(c)>2:
					poids[c[3]].append(c[-1])
					if c[3]==identifiantRelation:
						if int(c[-1])>0:
							motsCorrects[key]=value

				j+=1	
					

			if nat==False:
				p=[]
				for value in poids.values():
					if len(value) >1:
						p.append(value[0])
						motsCorrects[key]=max(p)
			


		else :
			print("le mot", key, "n'existe pas dans JDM.")
	return motsCorrects





derivationTerme(terme)


motsRezoDump=generationMotsJDM()

motsValides={}
for cle,valeur in resultat.items():
	if cle in motsRezoDump:
		motsValides[cle]=valeur



motsCorrects={}
print(u'mots generes a partir du terme "'+terme +'":\n', verificationNature(motsValides))

